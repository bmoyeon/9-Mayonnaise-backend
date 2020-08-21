import json

from django.views import View
from django.http import (
    JsonResponse,
    HttpResponse
)

from .models import (
    Menu,
    Category,
    Product,
    ProductSeries
)

class MenuView(View):
    def get(self, request):
        try:
            menus = Menu.objects.all()
            menu_list = [{
                'menu_id'   : menu.id,
                'menu_name' : menu.name
            } for menu in menus]
            return JsonResponse({'menu_list' : menu_list}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class CategoryView(View):
    def get(self, request):
        try:
            if 'menu_id' not in request.GET.keys():
                raise KeyError
            categories = Category.objects.filter(menu = request.GET.get('menu_id'))

            category_list = [{
                'category_id'   : category.id,
                'category_name' : category.name
            } for category in categories]
            return JsonResponse({'category_list' : category_list}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class ProductListView(View):
    def get(self, request):
        try:
            pair = {}
            if 'menu_id' in request.GET.keys():
                menu_id = request.GET.get('menu_id')
                pair['productpair__pair__menu'] = menu_id
                if not Menu.objects.filter(id = menu_id).exists():
                    return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status = 404)

            if 'category_id' in request.GET.keys():
                category_id = request.GET.get('category_id')
                pair['productpair__pair__category'] = category_id
                if not Category.objects.filter(id = category_id).exists():
                    return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status = 404)

            offset = int(request.GET.get('offset', 0))
            limit = int(request.GET.get('limit', 16))

            products = Product.objects.filter(**pair).prefetch_related(
                'producttag_set__tag',
                'image_set')

            search = request.GET.get('search', None)
            if search:
                products = products.filter(name_ko__icontains = search)

            sort = request.GET.get('sort', None)
            if sort == 'high_price':
                products = products.order_by('-price')
            elif sort == 'low_price':
                products = products.order_by('price')
            elif sort == 'new':
                products = products.order_by('-created_at')

            product_list = [{
                'product_id'      : product.id,
                'product_name_ko' : product.name_ko,
                'product_tag'     : [tag_name.tag.name for tag_name in product.producttag_set.all()],
                'product_image'   : product.image_set.get(is_main_img=True).image_url
            } for product in products[offset : offset + limit]]
            return JsonResponse({'product_list' : product_list}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALIDE_KEY'}, status = 400)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            if not Product.objects.filter(id = product_id).exists():
                return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status = 404)

            product = Product.objects.prefetch_related(
                'producttag_set__tag',
                'image_set',
                'productseries_set__series'
            ).get(id = product_id)

            series_id = None
            if product.productseries_set.filter(product = product_id).exists():
                series_id = product.productseries_set.get(product = product_id).series_id
            series = ProductSeries.objects.filter(series = series_id).prefetch_related('product__image_set')

            product_info = {
                'product_id'          : product.id,
                'product_name_ko'     : product.name_ko,
                'product_name_en'     : product.name_en,
                'product_tag'         : [tag_name.tag.name for tag_name in product.producttag_set.all()],
                'product_description' : product.description,
                'product_price'       : product.price,
                'product_volume'      : product.volume,
                'product_images'      : [images.image_url for images in product.image_set.all()],
                'product_ingredient'  : product.ingredient,
                'product_feature'     : product.feature.replace("src=\"", "src=\"https://www.laneige.com"),
                'product_series'      : [{
                    'product_id'      : series_product.product_id,
                    'product_name_ko' : series_product.product.name_ko,
                    'product_image'   : series_product.product.image_set.get(is_main_img=1).image_url,
                    'step'            : series_product.step
                } for series_product in series]
            }

            if not product_info['product_series']:
                del product_info['product_series']

            return JsonResponse({'product_info' : product_info}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALIDE_KEY'}, status = 400)
