from rest_framework import viewsets, pagination
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from home.models import Products


# Create your views here.


def index(request):
    return render(request, 'main/index_page.html')

def product_list(request):
    products = Products.objects.all().order_by('price')[:15]# :5 = last 15 # '-price' so'oodi
    # number_of_products = products.count()
    return render(request, 'main/product_list.html', {
        # 'number_of_products': number_of_products,
        'product': products
    })




def product_detail(request, slug):
    product = get_object_or_404(Products, slug=slug)
    return render(request, 'main/product-details.html', {
        'product': product
    })

def contact_page (request):
    return render(request, 'main/contact_page.html')

def site_header_partial(request):
    return render(request, 'shared/site_header_partial.html')

def site_footer_partial(request):
    return render(request, 'shared/site_footer_partial.html')