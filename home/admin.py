from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from home import models
# Register your models here.

@admin.register(models.Products)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    list_display = ('title', 'price', 'quantity', 'get_categories', 'last_update', 'is_active', 'image_preview')
    list_filter = ('title', 'category', 'is_active')
    list_editable = ('price', 'quantity', 'is_active')
    search_fields = ('title', 'price', 'quantity', 'category__name')
    ordering = ('-price',)
    date_hierarchy = 'last_update'

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    get_categories.short_description = 'Categories'

    def get_product_tag(self, obj):
        return ", ".join([tag.title for tag in obj.tags.all()])
    get_product_tag.short_description = 'Tags'

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "No Image"

    image_preview.short_description = 'تصویر'
        # Set a user-friendly column name in the admin panel

@admin.register(models.ProductPublisher)
class ProductPublisherAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)
    # list_filter = ('is_active',)
    ordering = ('title',)


@admin.register(models.ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    ordering = ('title',)

@admin.register(models.ProductsInfo)
class ProductsInfoAdmin(admin.ModelAdmin):
    list_display = (f'get_product_title', 'seller_name', 'writer', 'publisher', 'print', 'translator', 'pages', 'language')
    search_fields = ('seller_name', 'writer', 'print', 'translator', 'pages', 'language')
    list_filter = ('seller_name', 'writer', 'publisher', 'print', 'translator', 'pages', 'language')
    ordering = ('seller_name',)

    def get_product_title(self, obj):
        if obj.Product_Information:
            return obj.Product_Information.title
        return "No Product Associated"

        # Set a user-friendly column name in the admin panel

    get_product_title.short_description = 'Product Title'

@admin.register(models.Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')
    search_fields = ('name', 'content')
    list_filter = ('name',)
    ordering = ('name',)

@admin.register(models.Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('email', 'phone')
    ordering = ('username',)

@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'postal_code', 'home_phone')
    search_fields = ('user__username', 'address', 'postal_code')
    list_filter = ('postal_code', 'home_phone')
    ordering = ('user__username',)
