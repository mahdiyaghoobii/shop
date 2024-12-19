from django.contrib import admin
from home import models
# Register your models here.
@admin.register(models.Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity', 'is_done')
    list_filter = ('title', 'price', 'quantity', 'is_done')
    search_fields = ('title', 'price', 'quantity')
    ordering = ('-price',)
