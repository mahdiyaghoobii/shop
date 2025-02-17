from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from django.utils import timezone

from .models import Discount, Categories, Products


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


@receiver(m2m_changed, sender=Products.category.through)
def update_products_on_category_change(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        instance.save()

