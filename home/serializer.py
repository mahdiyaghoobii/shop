from django.contrib.auth import get_user_model
from rest_framework import serializers
from unicodedata import category
from account.models import User
from . import models
from rest_framework import serializers
from account.models import User
from django.contrib.auth.password_validation import validate_password

from .admin import ProductsInfoAdmin


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class ProductInfoPublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductPublisher
        fields = ('title', 'ia_active')


class ProductsInfoSerializer(serializers.ModelSerializer):
    publisher = ProductInfoPublisherSerializer()

    class Meta:
        model = models.ProductsInfo
        fields = ('seller_name', 'author', 'publisher', 'print', 'translator', 'pages', 'language')


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categories
        fields = '__all__'


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductTag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    Info = ProductsInfoSerializer()
    category = ProductCategorySerializer(many=True)
    tags = ProductTagSerializer(many=True)
    image = ImageSerializer()

    class Meta:
        model = models.Products
        fields = (
            'title', 'price', 'discounted_price', 'quantity', 'slug', 'sell_count', 'is_active',
            'last_update', 'rate', 'Info', 'category', 'image', 'tags')


class MostSellProductSerializer(serializers.ModelSerializer):
    Info = ProductsInfoSerializer()
    image = ImageSerializer()

    class Meta:
        model = models.Products
        fields = ('title', 'price', 'discounted_price', 'Info',
                  'image', 'sell_count', 'slug', 'rate')
    # def get_image_url(self, product):
    #     if product.image:
    #         return 'https://127.0.0.1:8000' + product.image.url
    #     return None


class PopularProductSerializer(serializers.ModelSerializer):
    Info = ProductsInfoSerializer()
    image = ImageSerializer()

    class Meta:
        model = models.Products
        fields = ('title', 'price', 'discounted_price', 'Info',
                  'image', 'sell_count', 'slug', 'rate')


class SliderSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = models.Slider
        fields = ('title', 'description', 'is_active', 'order', 'image')

    # def get_image_url(self, slider):
    #     if slider.image:
    #         return 'https://127.0.0.1:8000' + slider.image.url
    #     return None
