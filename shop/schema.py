import graphene
from graphene_django.types import DjangoObjectType
from home.models import Products, Categories, ProductsInfo, Discount, ProductTag, ProductPublisher, Image, Slider
from home.views import CategoryList

class SliderType(DjangoObjectType):
    class Meta:
        model = Slider

class ProductPublisherType(DjangoObjectType):
    class Meta:
        model = ProductPublisher

class ImageType(DjangoObjectType):
    class Meta:
        model = Image

class ProductTagType(DjangoObjectType):
    class Meta:
        model = ProductTag

class DiscountType(DjangoObjectType):
    class Meta:
        model = Discount

class ProductType(DjangoObjectType):
    class Meta:
        model = Products

class ProductsInfoType(DjangoObjectType):
    class Meta:
        model = ProductsInfo

class CategoryType(DjangoObjectType):
    class Meta:
        model = Categories

class Query(graphene.ObjectType):
    all_books = graphene.List(ProductType)
    top_selling_products = graphene.List(ProductType, limit=graphene.Int(default_value=10))
    category_list = graphene.List(CategoryType)
    all_Image = graphene.List(ImageType)

    def resolve_all_Image(self, info):
        return Image.objects.all()
    def resolve_all_books(self, info):
        return Products.objects.all()
    def resolve_top_selling_products(self, info, limit):
        return Products.objects.filter(is_active=True).order_by('-sellCount')[:limit]
    def  resolve_category_list(self, info):
        return Categories.objects.all()

schema = graphene.Schema(query=Query)