from django.contrib import admin
from . import models

@admin.register(models.User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('email', 'phone')
    ordering = ('username',)
# Register your models here.
