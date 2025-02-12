from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# class Customers(AbstractUser):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True, blank=True, null=True)
#     password = models.CharField(max_length=100)  # Note: Store hashed passwords for security
#     phone = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.name