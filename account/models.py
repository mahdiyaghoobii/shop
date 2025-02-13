from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name='شماره تلفن')
    email_active_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='کد فعال سازی ایمیل')
    phone_active_code = models.CharField(max_length=4, blank=True, null=True, verbose_name='کد فعال سازی موبایل')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return self.username