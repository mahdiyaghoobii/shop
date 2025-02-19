import os
import django
from django.conf import settings
from faker import Faker
from random import randint, choice
from django.core.files import File


# تنظیمات جنگو را بارگذاری کنید
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'D:/py/django-pr/shop/shop/settings.py')
django.setup()
from home.models import (
    Products, Categories, ProductTag,
    ProductPublisher, ProductsInfo, Image, Slider
)

fake = Faker('fa_IR')  # فارسی سازی دیتا


def create_categories():
    # ایجاد 5 دسته‌بندی نمونه
    for _ in range(5):
        Categories.objects.get_or_create(
            name=fake.word(),
            url_title=fake.slug(),
            content=fake.paragraph(),
            is_active=fake.boolean()
        )


def create_tags():
    # ایجاد 5 تگ نمونه
    for _ in range(5):
        ProductTag.objects.get_or_create(
            title=fake.word(),
            description=fake.sentence()
        )


def create_publishers():
    # ایجاد 5 انتشارات نمونه
    for _ in range(5):
        ProductPublisher.objects.get_or_create(
            title=fake.company(),
            ia_active=fake.boolean()
        )


def create_images():
    # ایجاد 10 تصویر نمونه (با تصویر پیش‌فرض)
    for _ in range(10):
        img = Image.objects.create(
            title=fake.word(),
        )
        # میتوانید از تصاویر واقعی استفاده کنید
        img.image_url.save(f'{fake.uuid4()}.png', File(open('static/default.png', 'rb')))  # مسیر تصویر پیش‌فرض


def create_products():
    categories = Categories.objects.all()
    tags = ProductTag.objects.all()
    publishers = ProductPublisher.objects.all()
    images = Image.objects.all()

    for _ in range(10):
        # ایجاد اطلاعات تکمیلی محصول
        product_info = ProductsInfo.objects.create(
            seller_name=fake.company(),
            author=fake.name(),
            publisher=choice(publishers),
            print=f"چاپ {randint(1, 10)}",
            translator=fake.name(),
            pages=randint(50, 500),
            language=choice(["en", "fa", "ar"])
        )

        # ایجاد محصول
        product = Products.objects.create(
            title=fake.sentence(nb_words=3),
            price=randint(10000, 1000000),
            discounted_price=randint(10000, 1000000),
            content=fake.paragraph(nb_sentences=5),
            Info=product_info,
            quantity=randint(0, 100),
            slug=fake.slug(),
            sell_count=randint(0, 1000),
            is_active=fake.boolean(),
            image=choice(images),
            is_deleted=fake.boolean()
        )

        # افزودن دسته‌بندی و تگ‌ها
        product.category.set(fake.random_elements(elements=categories, length=2, unique=True))
        product.tags.set(fake.random_elements(elements=tags, length=3, unique=True))


def main():
    print("ایجاد دسته‌بندی‌ها...")
    create_categories()

    print("ایجاد تگ‌ها...")
    create_tags()

    print("ایجاد انتشارات...")
    create_publishers()

    print("ایجاد تصاویر...")
    create_images()

    print("ایجاد محصولات...")
    create_products()

    print("تولید داده‌ها با موفقیت انجام شد!")


if __name__ == '__main__':
    main()