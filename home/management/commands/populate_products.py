import random
from django.core.management.base import BaseCommand
from faker import Faker
from home.models import Products, Categories, ProductTag, ProductPublisher, ProductsInfo

class Command(BaseCommand):
    help = 'Populate the database with random products'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create some categories, publishers, and tags if they don't exist
        categories = [Categories.objects.get_or_create(name=fake.word())[0] for _ in range(5)]
        publishers = [ProductPublisher.objects.get_or_create(title=fake.company())[0] for _ in range(5)]
        tags = [ProductTag.objects.get_or_create(title=fake.word())[0] for _ in range(5)]

        for _ in range(10):  # Change this number to create more or fewer products
            # Create ProductsInfo
            product_info = ProductsInfo.objects.create(
                seller_name=fake.company(),
                writer=fake.name(),
                publisher=random.choice(publishers),
                print=fake.word(),
                translator=fake.name(),
                pages=random.randint(50, 500),
                language=random.choice([("en", "English"), ("fa", "Farsi"), ("ar", "Arabic")])
            )

            # Create Products
            product = Products.objects.create(
                title=fake.catch_phrase(),
                price=random.randint(10000, 100000),
                price_after_discount=random.randint(5000, 90000),
                content=fake.text(),
                Info=product_info,
                quantity=random.randint(1, 100),
                slug=fake.slug(),
                sell_count=random.randint(0, 100),
                is_active=True,
                image='default.png',  # You can set a default image or generate random image paths
                is_deleted=False
            )

            # Add random categories and tags
            product.category.set(random.sample(categories, random.randint(1, 3)))  # Randomly assign 1 to 3 categories
            product.tags.set(random.sample(tags, random.randint(1, 3)))  # Randomly assign 1 to 3 tags

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with random products.'))
