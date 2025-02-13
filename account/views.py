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
from home.models import Products
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from home.serializer import RegisterSerializer, ProductSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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
