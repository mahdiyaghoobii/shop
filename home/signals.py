import os

from slugify import slugify
from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models.signals import post_save, pre_delete, m2m_changed, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Discount, Categories, Products
from django.db.models import F


# ایجاد یک scheduler
# scheduler = BackgroundScheduler()
#
#
# @receiver(post_save, sender=Discount)
# def schedule_discount_expiry(sender, instance, created, **kwargs):
#     if created and instance.end_date:  # فقط برای تخفیف‌های جدید و دارای end_date
#         # حذف تسک قبلی اگر وجود داشته باشد
#         job_id = f"discount_{instance.id}"
#         if scheduler.get_job(job_id):
#             scheduler.remove_job(job_id)
#
#         # برنامه‌ریزی تسک جدید
#         scheduler.add_job(
#             deactivate_discount,
#             'date',
#             run_date=instance.end_date,
#             args=[instance.id],
#             id=job_id
#         )
#
#         # شروع scheduler اگر هنوز شروع نشده باشد
#         if not scheduler.running:
#             scheduler.start()
#
#
# def deactivate_discount(discount_id):
#     try:
#         discount = Discount.objects.get(id=discount_id)
#         if timezone.now() >= discount.end_date:
#             discount.is_active = False
#             discount.save()
#     except Discount.DoesNotExist:
#         pass

@receiver(post_save, sender=Discount)
def handle_discount_change(sender, instance, **kwargs):
    # دسته‌های مرتبط با این تخفیف
    related_categories = Categories.objects.filter(discount=instance)

    if not instance.is_active:
        # اگه تخفیف غیرفعال باشه، تخفیف رو از دسته‌ها حذف کن
        # Categories.objects.filter(discount=instance).update(discount=None)
        # محصولات مرتبط رو به‌روزرسانی کن (قیمت تخفیف‌خورده به None)
        for category in related_categories:
            for product in Products.objects.filter(category=category):
                update_discounted_price(product)
    else:
        # اگه تخفیف فعال باشه، محصولات مرتبط رو به‌روزرسانی کن
        for category in related_categories:
            for product in Products.objects.filter(category=category):
                update_discounted_price(product)


@receiver(post_save, sender=Categories)
def update_product_prices(sender, instance, **kwargs):
    for product in Products.objects.filter(category=instance):
        update_discounted_price(product)


# hale
@receiver(pre_delete, sender=Discount)
def handle_discount_deletion(sender, instance, **kwargs):
    Categories.objects.filter(discount=instance).update(discount=None)


# firdst update_discounted_price
@receiver(pre_save, sender=Products)
def update_product_discounted_price(sender, instance, **kwargs):
    # print("product post save")
    # if instance.discounted_price:
    #     print("product discounted price", instance.discounted_price)
    # elif not instance.discounted_price:
    update_discounted_price(instance)


@receiver(m2m_changed, sender=Products.category.through)
def update_products_on_category_change(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        update_discounted_price(instance)  # Call the helper function


def update_discounted_price(instance, *args, **kwargs):
    valid_discounts = []

    for category in instance.category.all().prefetch_related('discount'):
        if category.discount and category.discount.is_active:
            valid_discounts.append(category.discount.percentage)
        else:
            valid_discounts.append(0)

    max_discount = max(valid_discounts) if valid_discounts else 0
    print(f"Max discount for {instance.title}: {max_discount}")
    if max_discount > 0:
        discounted_price = int(instance.price * (100 - max_discount) // 100)
        Products.objects.filter(pk=instance.pk).update(discounted_price=discounted_price)
        print(f"Setting discounted price to {discounted_price}")
    else:
        Products.objects.filter(pk=instance.pk).update(discounted_price=None)
        print(f"Setting discounted price to None")


@receiver(pre_save, sender=Products)
def fa_slugify(sender, instance, **kwargs):
    if not instance.slug:
        if not instance.title:
            pass
        slugged = slugify(instance.title, allow_unicode=True)
        count = 1
        while Products.objects.filter(slug=slugged).exists():
            slugged = slugged + f'{count}'
            count += 1
        instance.slug = slugged
