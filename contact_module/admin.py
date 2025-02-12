from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.contact_us)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'full_name', 'created_at', 'is_read_by_admin')
    search_fields = ('title', 'email', 'full_name', 'created_at', 'is_read_by_admin')
    list_filter = ('title', 'email', 'full_name', 'created_at', 'is_read_by_admin')
    ordering = ('created_at',)
    date_hierarchy = 'created_at'
    list_editable = ('is_read_by_admin',)
    list_display_links = ('title', 'email', 'full_name')
    list_per_page = 10
    list_max_show_all = 100
    # list_select_related = ('title', 'email', 'full_name', 'created_at', 'is_read_by_admin')