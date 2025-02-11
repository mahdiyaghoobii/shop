from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View, generic
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets, status, pagination, permissions
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Products
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .serializer import RegisterSerializer, ProductSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# class CustomPagination(pagination.PageNumberPagination):
#     page_size = 1  # Number of items per page
#     page_size_query_param = 'page_size'
#     max_page_size = 100

def signin_user(request):
    return render(request, 'home/signin.html')

class RegisterView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User created successfully",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # You can customize the response here if needed
        return response

class productlist(APIView):
    def get(self, request: Request):
        prlist = Products.objects.all()
        # paginator = CustomPagination()
        # paginated_prlist = paginator.paginate_queryset(prlist, request)
        product_serializer = ProductSerializer(prlist, many=True)
        # return paginator.get_paginated_response(product_serializer.data)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

class ProductFilter(APIView):
    def get(self, request: Request):
        # Get query parameters for 'tag' and 'category'
        tag_title = request.query_params.get('tag', None)
        category_title = request.query_params.get('category', None)
        price_min = int(request.query_params.get('min', default=0))
        price_max = int(request.query_params.get('max', default=9999999999999999999999))
        # Start with all products
        prlist = Products.objects.all()
        # Apply filters based on query parameters
        if tag_title is not None:   #tag filter
            prlist = prlist.filter(tags__title=tag_title)
            if not prlist.exists():
                return Response({"error": f"No products found for tag: {tag_title}."}, status=status.HTTP_404_NOT_FOUND)
        if category_title is not None: #category filter
            prlist = prlist.filter(category__name=category_title)
            if not prlist.exists():
                return Response({"error": f"No products found for category: {category_title}."}, status=status.HTTP_404_NOT_FOUND)
        if price_min is not None and price_max is not None: #price limits
            prlist = prlist.filter(price__gte=price_min, price__lte=price_max)
            if not prlist.exists():
                return Response({"error": f"No products found for this price range: {price_min} - {price_max}."},status=status.HTTP_404_NOT_FOUND)
        product_serializer = ProductSerializer(prlist, many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

class product_most_sells(APIView):
    def get(self, request: Request):
        mslist = Products.objects.all().order_by('-sell_count')[:10]
        product_most_sells_serilizer = ProductSerializer(mslist, many=True)
        return Response(product_most_sells_serilizer.data, status=status.HTTP_200_OK)