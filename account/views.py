from home.serializer import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.core.cache import cache


class SigninUser(APIView):
    authentication_classes = []  # غیرفعال کردن احراز هویت
    permission_classes = [AllowAny]  # اجازه دسترسی به همه

    def post(self, request):
        # گرفتن اطلاعات ورودی از درخواست
        username = request.data.get('username')
        password = request.data.get('password')

        # احراز هویت کاربر
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # لاگین کاربر
            login(request, user)

            # تولید توکن
            refresh = RefreshToken.for_user(user)

            # تنظیم پاسخ
            response = Response({
                "message": "User logged in successfully.",
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

            # ذخیره توکن در HTTP-Only Cookie
            response.set_cookie(
                key='token',
                value=str(refresh),
                httponly=True,
                secure=True,  # فقط در HTTPS ارسال شود
                samesite='Strict',  # امنیت بیشتر
                max_age=7 * 24 * 60 * 60  # عمر کوکی: 7 روز
            )

            # بازگردانی پاسخ
            return response
        # request.session['user_id'] = request.user.id
        # cache.set('my_key',str(RefreshToken.for_user(user)), timeout=1200)
        # ارسال پاسخ خطا در صورت احراز هویت ناموفق
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


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
        if request.user.is_authenticated:
            logout(request)

        response = Response({"message": "User signed out successfully."}, status=200)
        response.delete_cookie('token')
        return response


class RefreshTokenView(APIView):
    authentication_classes = []  # غیرفعال کردن احراز هویت
    permission_classes = [AllowAny]  # اجازه دسترسی به همه

    def get(self, request):
        refresh_token = request.COOKIES.get('token')

        if not refresh_token:
            return Response({"error": "Refresh token not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # تجدید توکن
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response({
                "message": "Token refreshed successfully.",
                "access_token": access_token,
            }, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid or expired refresh token."}, status=status.HTTP_401_UNAUTHORIZED)
