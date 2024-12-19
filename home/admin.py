from django.contrib import admin
from home import models
# Register your models here.
@admin.register(models.Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity', 'is_done')
    list_filter = ('title', 'price', 'quantity', 'is_done')
    search_fields = ('title', 'price', 'quantity')
    ordering = ('-price',)

@admin.register(models.Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('email', 'phone')
    ordering = ('name',)

@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'postal_code', 'home_phone')
    search_fields = ('user__name', 'address', 'postal_code')
    list_filter = ('postal_code', 'home_phone')
    ordering = ('user__name',)
