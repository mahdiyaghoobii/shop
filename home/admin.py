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
    list_display = ('title',)
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
    list_display = (
        f'get_product_title', 'seller_name', 'author', 'publisher', 'print', 'translator', 'pages', 'language')
    search_fields = ('seller_name', 'author', 'print', 'translator', 'pages', 'language')
    list_filter = ('seller_name', 'author', 'publisher', 'print', 'translator', 'pages', 'language')
    ordering = ('seller_name',)

    def get_product_title(self, obj):
        if obj.Product_Information:
            return obj.Product_Information.title
        return "No Product Associated"

        # Set a user-friendly column name in the admin panel

    get_product_title.short_description = 'Product Title'


@admin.register(models.Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'get_count')
    search_fields = ('name', 'content')
    list_filter = ('name',)
    ordering = ('name',)

    def get_count(self, obj):
        return obj.products_set.count()


# @admin.register(models.Users)
# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'phone')
#     search_fields = ('username', 'email', 'phone')
#     list_filter = ('email', 'phone')
#     ordering = ('username',)
#
# @admin.register(models.UserInfo)
# class UserInfoAdmin(admin.ModelAdmin):
#     list_display = ('user', 'address', 'postal_code', 'home_phone')
#     search_fields = ('user__username', 'address', 'postal_code')
#     list_filter = ('postal_code', 'home_phone')
#     ordering = ('user__username',)


from django.contrib import admin
from django.utils.html import format_html
from .models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    # تنظیمات نمایش لیست
    list_display = (
        'colored_title',
        'percentage_bar',
        'status_indicator',
        'date_range',
        'is_active'
    )
    list_filter = (
        ('start_date', admin.DateFieldListFilter),
        ('end_date', admin.DateFieldListFilter),
        'is_active',
    )
    search_fields = ('title', 'percentage')
    ordering = ('-start_date',)
    list_editable = ('is_active',)
    list_per_page = 20
    date_hierarchy = 'start_date'

    # تنظیمات فرم ویرایش
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'percentage', ('start_date', 'end_date'))
        }),
        ('تنظیمات پیشرفته', {
            'classes': ('collapse',),
            'fields': ('is_active',),
        }),
    )

    # متدهای کمکی برای نمایش زیباتر
    def colored_title(self, obj):
        return format_html(
            '<span style="color: #{};">{}</span>',
            '2196F3' if obj.is_active else 'FF5722',
            obj.title
        )

    colored_title.short_description = 'عنوان'

    def percentage_bar(self, obj):
        return format_html(
            '<div style="background: #e0e0e0; width: 100px; height: 20px; border-radius: 3px;">'
            '<div style="background: #4CAF50; width: {}%; height: 100%; border-radius: 3px;"></div>'
            '</div> {}%',
            obj.percentage,
            obj.percentage
        )

    percentage_bar.short_description = 'درصد تخفیف'

    def status_indicator(self, obj):
        color = '4CAF50' if obj.is_active else 'FF5722'
        text = 'فعال' if obj.is_active else 'غیرفعال'
        return format_html(
            '<div style="background: #{}; color: white; padding: 3px 8px; border-radius: 15px; display: inline-block;">{}</div>',
            color,
            text
        )

    status_indicator.short_description = 'وضعیت'

    def date_range(self, obj):
        if obj.start_date and obj.end_date:
            return f'{obj.start_date.strftime("%Y-%m-%d")} --- {obj.end_date.strftime("%Y-%m-%d")}'
        return '-'

    date_range.short_description = 'بازه زمانی'

    # متدهای پیشرفته
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('categories_set')

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_active:
            return False  # جلوگیری از حذف تخفیف‌های فعال
        return super().has_delete_permission(request, obj)


@admin.register(models.Slider)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order',)
    search_fields = ('title',)
    ordering = ('title',)
