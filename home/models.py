import django.utils.text
from django.db import models
from django.utils.text import slugify
from slugify import slugify as persian_slugify
from datetime import datetime
from django.db.models import JSONField
from shop import settings
# Create your models here.


class Info(models.Model):
    site_name = models.CharField(max_length=100)
    support_number = models.CharField(max_length=100)
    def __str__(self):
        return self.site_name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=100)  # Note: Store hashed passwords for security
    phone = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserInfo(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='info', default=None)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    home_phone = models.CharField(max_length=100)
    payment_info = JSONField(blank=True, default=list, help_text="Store detailed payment information as JSON", editable=False)

    def __str__(self):
        return self.user.phone  # Use the related user's phone number

    def save(self, *args, **kwargs):
        # Ensure the payment_info is a list if it's empty
        if not self.payment_info:
            self.payment_info = []
        super().save(*args, **kwargs)

class Products(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15, default=0, decimal_places=3, help_text='ریال', )
    price_after_discount = models.DecimalField(max_digits=15, default=None, decimal_places=3, blank=True, null=True)
    content = models.TextField()
    writer = models.CharField(max_length=100, default=None)
    publisher = models.CharField(max_length=100, default=None)
    print = models.CharField(max_length=100, default=None)
    translator = models.CharField(max_length=100, blank=True, null=True)
    pages = models.IntegerField(default=0)
    language = models.CharField(max_length=100, choices={"en" : "English", "fa" : "Farsi", "ar" : "Arabic"}, default='fa')
    quantity = models.PositiveIntegerField(default=0)
    # slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    rate = models.IntegerField(default=0, editable=False)
    seller_name = models.CharField(max_length=100, default="کتابخانه", blank=True, null=True)
    sell_count = models.IntegerField(default=0)
    is_done = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now=True, blank=True, null=True, ) # problem:
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    image_path = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if self.image:
    #
    #
    #         self.image_path = 'images/' + self.image.name
    #     self.slug = slugify(self.title)
    #     super(blog, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.image:
            if self.title:
                if self.title.isascii():  # Check if title is in English
                    slugified_title = slugify(self.title)
                else:
                    slugified_title = persian_slugify(self.title)
                self.image_path = f'images/{slugified_title}/{self.image.name}'
            else:
                self.image_path = f'images/{self.image.name}'
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)