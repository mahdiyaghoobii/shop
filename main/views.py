from rest_framework import viewsets, pagination
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from home.models import Products


# Create your views here.


def index(request):
    return render(request, 'main/index_page.html')
def contact_page (request):
    return render(request, 'main/contact_page.html')

def site_header_partial(request):
    return render(request, 'shared/site_header_partial.html')

def site_footer_partial(request):
    return render(request, 'shared/site_footer_partial.html')