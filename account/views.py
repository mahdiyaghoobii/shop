from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View, generic
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
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
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def signin_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User logged in successfully.",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=200)
        return Response({"error": "Invalid credentials."}, status=400)
    return Response({"error": "Method not allowed."}, status=405)


class RegisterView(APIView):
    authentication_classes = []  # غیرفعال کردن احراز هویت
    permission_classes = [AllowAny]  # اجازه دسترسی به همه
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


class SignoutUser(APIView):
    def post(self, request):
        response = Response({"message": "User signed out successfully."}, status=200)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
