from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from home import admin
from . import views

urlpatterns = [
    # path('best_product/', views.BestProductSlider.as_view(), name='best_product'),
    path('list-product/', views.productlist.as_view(), name='product-list'),
    path('most-sells-products/', views.product_most_sells.as_view(), name='most-sells-products'),
    path('filter/', views.ProductFilter.as_view(), name='my_view'),
    path('slider/', views.Slides.as_view(), name='slider'),
    path('<slug:slug>/', views.Product_detail.as_view(), name='product_detail'),

    # path('signin/', views.signin_user, name='signin'),
    # path('signup/', views.signup_user, name='signup'),
]
