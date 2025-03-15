from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('site_header_partial', views.site_header_partial, name='site_header_partial'),
    # path('products', views.product_list, name='product_list'),
    # path('<slug:slug>', views.product_detail, name='product_detail'),
]