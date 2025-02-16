from django.contrib.auth import get_user_model
from rest_framework import serializers
from account.models import User
from . import models
from rest_framework import serializers
from account.models import User
from django.contrib.auth.password_validation import validate_password

from .admin import ProductsInfoAdmin

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

class ProductsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductsInfo
        fields = '__all__'

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
    category = ProductCategorySerializer()
    tags = ProductTagSerializer(many=True)
    class Meta:
        model = models.Products
        fields = '__all__'

class MostSellProductSerializer(serializers.ModelSerializer):
    # Info = ProductsInfoSerializer()
    # category = ProductCategorySerializer()
    # tags = ProductTagSerializer(many=True)
    class Meta:
        model = models.Products
        fields = 'title', 'price', 'price_after_discount', 'image', 'sell_count'
