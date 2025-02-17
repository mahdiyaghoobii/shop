import django.utils.text
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.fields import CharField
from django.template.defaultfilters import title
from django.utils import timezone
from django.utils.text import slugify
from slugify import slugify as persian_slugify
from datetime import datetime
from django.db.models import JSONField
from shop import settings
from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.dispatch import receiver


# Create your models here.


class Info(models.Model):
    site_name = models.CharField(max_length=100)
    support_number = models.CharField(max_length=100)

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# class Users(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True, blank=True, null=True)
#     password = models.CharField(max_length=100)  # Note: Store hashed passwords for security
#     phone = models.CharField(max_length=100, unique=True)
#
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_set',  # Unique related_name
#         blank=True,
#         verbose_name='groups',
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_set',  # Unique related_name
#         blank=True,
#         verbose_name='user permissions',
#         help_text='Specific permissions for this user.',
#     )
#
#     def __str__(self):
#         return self.username

# class UserInfo(models.Model):
#     user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='info', default=None)
#     address = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=100)
#     home_phone = models.CharField(max_length=100)
#     payment_info = JSONField(blank=True, default=list, help_text="Store detailed payment information as JSON", editable=False)

# def __str__(self):
#     return self.user.phone  # Use the related user's phone number
#
# def save(self, *args, **kwargs):
#     # Ensure the payment_info is a list if it's empty
#     if not self.payment_info:
#         self.payment_info = []
#     super().save(*args, **kwargs)


class Discount(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان', db_index=True)
    percentage = models.PositiveIntegerField(verbose_name="درصد تخفیف")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پایان')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'

    def is_valid(self):
        now = timezone.now()
        start_ok = self.start_date is None or self.start_date <= now
        end_ok = self.end_date is None or self.end_date >= now
        return self.is_active and start_ok and end_ok

    def __str__(self):
        return self.title


class Categories(models.Model):
    name = models.CharField(max_length=100, verbose_name='عنوان', db_index=True)
    url_title = models.CharField(max_length=100, null=True, verbose_name='عنوان در url', db_index=True)
    content = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="تخفیف")
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')

    class Meta:
        verbose_name = 'سته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name


class ProductTag(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان تگ', db_index=True)
    description = models.CharField(null=True, blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ ها'  # tag ----> "tags"

    def __str__(self):
        return self.title


class ProductPublisher(models.Model):
    title = models.CharField(max_length=100, verbose_name='نام انتشارات', db_index=True)
    ia_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')

    class Meta:
        verbose_name = 'انتشارات'
        verbose_name_plural = 'انتشارات'

    def __str__(self):
        return self.title


class ProductsInfo(models.Model):
    seller_name = models.CharField(max_length=100, default="کتابخانه", blank=True, null=True, verbose_name='فروشنده')
    author = models.CharField(max_length=100, default=None, verbose_name='نویسنده')
    publisher = models.ForeignKey(ProductPublisher, on_delete=models.CASCADE, default=None, verbose_name='انتشارات')
    print = models.CharField(max_length=100, default=None, verbose_name='نوبت چاپ')
    translator = models.CharField(max_length=100, blank=True, null=True, verbose_name='مترجم')
    pages = models.IntegerField(default=0, verbose_name='تعداد صفحات')
    language = models.CharField(max_length=100, choices=[("en", "English"), ("fa", "Farsi"), ("ar", "Arabic")],
                                default='fa', verbose_name='زبان')

    def __str__(self):
        return f'{self.seller_name} - {self.author}'

    class Meta:
        verbose_name = 'اطلاعات محصول'
        verbose_name_plural = 'اطلاعات محصولات'


class Products(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان', db_index=True)
    price = models.IntegerField(default=0, help_text='تومان', verbose_name='قیمت', db_index=True)
    discounted_price = models.IntegerField(null=True, blank=True, default=0, help_text='تومان',
                                           verbose_name='قیمت پس از تخفیف', db_index=True)
    content = models.TextField(null=True, verbose_name='توضیحات')
    Info = models.OneToOneField(ProductsInfo, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='Product_Information', verbose_name='اطلاعات تکمیلی')
    category = models.ManyToManyField(Categories, blank=True, verbose_name='دسته بندی')
    quantity = models.PositiveIntegerField(default=0, verbose_name='تعداد')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, blank=True, null=True,
                            verbose_name='عنوان در url')
    # rate = models.IntegerField(default=0, editable=False, verbose_name='امتیاز')
    sell_count = models.IntegerField(default=0, verbose_name='تعداد فروش')
    # test = models.CharField(null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    last_update = models.DateTimeField(auto_now=True, verbose_name='آخرین تغییرات', null=True)  # problem:
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='تصویر', default='default.png')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    tags = models.ManyToManyField(ProductTag, blank=True, verbose_name='تگ', default=None)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        valid_discounts = []

        for category in self.category.all().prefetch_related('discount'):
            if category.discount and category.discount.is_valid():
                valid_discounts.append(category.discount.percentage)

        max_discount = max(valid_discounts) if valid_discounts else 0

        if max_discount > 0:
            self.discounted_price = self.price * (100 - max_discount) // 100
        else:
            self.discounted_price = None

        super().save(*args, **kwargs)
