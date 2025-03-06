from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from home import admin
from . import views

urlpatterns = [
    # path('best_product/', views.BestProductSlider.as_view(), name='best_product'),
    path('clear_basket/', views.clear_basket.as_view(), name='clear_basket'),
    path('list-product/', views.productlist.as_view(), name='product-list'),
    path('most-sells-products/', views.product_most_sells.as_view(), name='most-sells-products'),
    path('popular-products/', views.popular_product.as_view(), name='popular-products'),
    path('setrate/', views.rating.as_view(), name='rating'),
    path('filter/', views.ProductFilter.as_view(), name='my_view'),
    path('slider/', views.Slides.as_view(), name='slider'),
    # path('<int:pk>/', views.Product_detail.as_view(), name='product_detail'),
    re_path(r'(?P<slug>[\w\-_۰-۹آ-ی]+)/', views.Product_detail.as_view(), name='product_detail'),
    path('add-to-basket/<slug:slug>/', views.add_basket.as_view(), name='add_to_basket'),

]
