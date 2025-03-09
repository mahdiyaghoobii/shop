from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets, status, pagination, permissions
from rest_framework.request import Request
from .models import Products, Slider
from .serializer import RegisterSerializer, ProductSerializer, MostSellProductSerializer, SliderSerializer


class CustomPagination(pagination.PageNumberPagination):
    page_size = 1  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class productlist(APIView):
    authentication_classes = []  # غیرفعال کردن JWT برای این ویو
    permission_classes = [AllowAny]  # اجازه دسترسی به همه کاربران

    def get(self, request: Request):
        prlist = Products.objects.all()
        # paginator = CustomPagination()
        # paginated_prlist = paginator.paginate_queryset(prlist, request)
        product_serializer = ProductSerializer(prlist, many=True)
        # return paginator.get_paginated_response(product_serializer.data)
        return Response(product_serializer.data, status=status.HTTP_200_OK)


class ProductFilter(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request: Request):
        # Get query parameters for 'tag' and 'category'
        tag_title = request.query_params.get('tag', None)
        category_url = request.query_params.get('category', None)
        price_min = int(request.query_params.get('min', default=0))
        price_max = int(request.query_params.get('max', default=9999999999999999999999))
        # Start with all products
        prlist = Products.objects.all()
        # Apply filters based on query parameters
        if tag_title is not None:  # tag filter
            prlist = prlist.filter(tags__title=tag_title)
            if not prlist.exists():
                return Response({"error": f"No products found for tag: {tag_title}."}, status=status.HTTP_404_NOT_FOUND)
        if category_url is not None:  # category filter
            prlist = prlist.filter(category__url_title=category_url)
            if not prlist.exists():
                return Response({"error": f"No products found for category: {category_url}."},
                                status=status.HTTP_404_NOT_FOUND)
        if price_min is not None and price_max is not None:  # price limits
            prlist = prlist.filter(price__gte=price_min, price__lte=price_max)
            if not prlist.exists():
                return Response({"error": f"No products found for this price range: {price_min} - {price_max}."},
                                status=status.HTTP_404_NOT_FOUND)
        product_serializer = ProductSerializer(prlist, many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)


class popular_product(APIView): #need pagination!!!!!!!!
    authentication_classes = []
    permission_classes = [AllowAny]
    def get(self, request: Request):
        product_list = Products.objects.filter(rate__gt=0).order_by('-rate')
        popular_prodiuct_serializer = ProductSerializer(product_list, many=True)
        return Response(popular_prodiuct_serializer.data, status=status.HTTP_200_OK)


class product_most_sells(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def get(self, request: Request):
        mslist = Products.objects.all().order_by('-sell_count')[:10]
        product_most_sells_serilizer = MostSellProductSerializer(mslist, many=True)
        return Response(product_most_sells_serilizer.data, status=status.HTTP_200_OK)


class Slides(APIView):
    authentication_classes = []  # غیرفعال کردن JWT برای این ویو
    permission_classes = [AllowAny]  # اجازه دسترسی به همه کاربران

    def get(self, request: Request):
        slide_images = Slider.objects.filter(is_active=True).order_by('order')[:5]

        # paginator = CustomPagination()
        # paginated_prlist = paginator.paginate_queryset(prlist, request)
        slider_serializer = SliderSerializer(slide_images, many=True)
        # return paginator.get_paginated_response(product_serializer.data)
        return Response(slider_serializer.data, status=status.HTTP_200_OK)


class Product_detail(APIView):
    authentication_classes = []  # غیرفعال کردن JWT برای این ویو
    permission_classes = [AllowAny]  # اجازه دسترسی به همه کاربران

    def get(self, request: Request, slug):
        try:
            product = Products.objects.get(slug=slug)
            product_serializer = ProductSerializer(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        except Products.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


class add_basket(APIView):
    authentication_classes = []  # غیرفعال کردن JWT برای این ویو
    permission_classes = [AllowAny]  # اجازه دسترسی به همه کاربران

    def get(self, request: Request, slug):
        try:
            product = Products.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        product_data = {
            'title': product.title,
            'price': str(product.price),
            'discounted_price': str(product.discounted_price) if product.discounted_price else None,
            'slug': product.slug,
            'quantity': 1
        }

        if 'basket' in request.session:
            basket = request.session['basket']
            if product_data['slug'] in basket:
                # اگر محصول از قبل در سبد وجود دارد، مقدار quantity را افزایش دهید
                basket[product_data['slug']]['quantity'] += 1
            else:
                # اگر محصول در سبد وجود ندارد، آن را اضافه کنید
                basket[product_data['slug']] = product_data

            request.session['basket'] = basket  # ذخیره تغییرات در session
            request.session.modified = True  # اعلام تغییر session به Django

        else:
            # اگر سبد وجود ندارد، یک سبد جدید ایجاد کنید و محصول را اضافه کنید
            request.session['basket'] = {product_data['slug']: product_data}
            request.session.modified = True  # اعلام تغییر session به Django

        cost, basket_items = 0, 0
        for item_key in request.session['basket']:
            item = request.session['basket'][item_key]
            basket_items += item['quantity']
            if item['discounted_price']:
                cost += int(item['discounted_price']) * int(item['quantity'])
            else:
                cost += int(item['price']) * int(item['quantity'])

        return Response({"message": f"Product added to basket. {request.session['basket']}", "cost": f"{str(cost)}",
                         "basket_items": f"{str(basket_items)}"}, status=status.HTTP_200_OK)


class clear_basket(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        if 'basket' in request.session:
            del request.session['basket']  # حذف سبد خرید از session
            request.session.modified = True  # اعلام تغییر session به Django
            return Response({"message": "Basket cleared."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Basket is already empty."},
                            status=status.HTTP_200_OK)  # optional: you can also return 404

class rating(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request: Request):
        rate_unrate = request.data.get('rate_unrate')
        # rate = request.POST.get('rate')
        slug = request.data.get('slug')
        print(request.data.get('rate_unrate'))
        product = Products.objects.get(slug=slug)
        # Rate
        rated_products = request.session.get('rated',[])

        if rate_unrate == 'rate':

            if product:
                product.rate += 1
                product.save()

                if product.pk not in rated_products:
                    rated_products.append(product.pk)
                    request.session['rated'] = rated_products
                else:
                    request.session['rated'] = [product.pk]
                request.session.save()

                return Response({"message": f"{slug}'s rate increased: {product.rate} , rated products: {request.session['rated']}"},
                               status=status.HTTP_200_OK)
            else:
                return Response({"message": f"there is no product with this slug: {slug}"},status=status.HTTP_404_NOT_FOUND)
        # UnRate
        elif rate_unrate == 'unrate':
            if product:
                product.rate -= 1
                if product.pk in rated_products:
                    rated_products.remove(product.pk)
                    request.session['rated'] = rated_products
                    request.session.save()
                if product.rate >= 0:
                    product.save()
                    return Response({"message": f"{slug}'s rate decreased: {product.rate} , rated products: {request.session['rated']}"},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"message": f"{slug}'s rate is also 0."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": f"there is no product with this slug: {slug}"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": f"there is no product with this slug: {slug}"}, status=status.HTTP_404_NOT_FOUND)