from rest_framework import serializers
from .models import Products, Users
# from django.contrib.auth import get_user_model
#
# User = get_user_model()

class products_serializer(serializers.ModelSerializer):
    # time_field = serializers.DateTimeField(format='%H:%M')  # فقط ساعت و دقیقه
    # date_field = serializers.DateTimeField(format='%Y-%m-%d')  # فقط تاریخ

    class Meta:
        model =  Products
        # fields = ['title', 'price', 'quantity','content', 'is_done', 'slug','time_field', 'date_field']
        fields = '__all__'
        # read_only_fields =

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

# class userserilizer(serializers.ModelSerializer):
#     todos = todoserilizer(read_only=True, many=True) # why todos? cause it's the "related name" in models.py
#
#
#     class Meta:
#         model = User
#         fields = '__all__'