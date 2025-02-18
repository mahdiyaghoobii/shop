from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from .models import Discount, Categories, Products
from django.db.models import F


# ایجاد یک scheduler
scheduler = BackgroundScheduler()


@receiver(post_save, sender=Discount)
def schedule_discount_expiry(sender, instance, created, **kwargs):
    if created and instance.end_date:  # فقط برای تخفیف‌های جدید و دارای end_date
        # حذف تسک قبلی اگر وجود داشته باشد
        job_id = f"discount_{instance.id}"
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)

        # برنامه‌ریزی تسک جدید
        scheduler.add_job(
            deactivate_discount,
            'date',
            run_date=instance.end_date,
            args=[instance.id],
            id=job_id
        )

        # شروع scheduler اگر هنوز شروع نشده باشد
        if not scheduler.running:
            scheduler.start()


def deactivate_discount(discount_id):
    try:
        discount = Discount.objects.get(id=discount_id)
        if timezone.now() >= discount.end_date:
            discount.is_active = False
            discount.save()
    except Discount.DoesNotExist:
        pass


@receiver(post_save, sender=Discount)
def update_products_on_discount_change(sender, instance, **kwargs):
    related_categories = Categories.objects.filter(discount=instance)
    for category in related_categories:
        for product in Products.objects.filter(category=category):
            product.save()


@receiver(post_save, sender=Categories)
def update_product_prices(sender, instance, **kwargs):
    for product in Products.objects.filter(category=instance):
        product.save()


@receiver(pre_delete, sender=Discount)
def handle_discount_deletion(sender, instance, **kwargs):
    Categories.objects.filter(discount=instance).update(discount=None)


@receiver(post_save, sender=Products)
def update_product_discounted_price(sender, instance, created, **kwargs):
    if created: # Only run this if the product is newly created
        update_discounted_price(instance) # Call the helper function

@receiver(m2m_changed, sender=Products.category.through)
def update_products_on_category_change(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        update_discounted_price(instance) # Call the helper function

def update_discounted_price(instance): # Helper function
    valid_discounts = []
    for category in instance.category.all().prefetch_related('discount'):
        if category.discount and category.discount.is_valid():  # Assuming is_valid() is defined
            valid_discounts.append(category.discount.percentage)

    max_discount = max(valid_discounts) if valid_discounts else 0

    if max_discount > 0:
        Products.objects.filter(pk=instance.pk).update(discounted_price=F('price') * (100 - max_discount) // 100)
    else:
        Products.objects.filter(pk=instance.pk).update(discounted_price=None)