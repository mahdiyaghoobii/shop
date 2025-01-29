from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from home import admin
from . import views

urlpatterns = [
    path('best_product/', views.BestProductSlider.as_view(), name='best_product'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
]