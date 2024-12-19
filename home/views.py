from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets, status
from rest_framework.request import Request
from .models import Products
from .serializer import products_serializer


# region cbv product

class BestProductSlider(APIView):

    def get(self,request: Request):
        best_product_slider = Products.objects.filter(is_done=True).order_by('sell_count').all()
        todo_serializer = products_serializer(best_product_slider, many= True)
        return Response(todo_serializer.data, status.HTTP_200_OK)
#endregion

# region viewset

class DetailProductView(APIView):
    def get(self,request: Request,pk):
        pass
#endregion



class HomePageView(viewsets.ModelViewSet):
    queryset =  Products.objects.order_by('pk').all()
    serializer_class = products_serializer