import json

from django.views import View
from django.http import (
    JsonResponse,
    HttpResponse
)

from .models import (
    Menu,
    Type,
    Category,
    ProductCategory,
    Product,
    ProductSeries
)

class ProductListView(View):
    def get(self, request):        
        try:
            search = request.GET.get('search')
            sort = request.GET.get('sort')
            offset = int(request.GET.get('offset', "0"))
            limit = int(request.GET.get('limit', "16"))
            filter_dict = {}
            if 'menu_id' in request.GET.keys():
                filter_dict['productcategory__category__menu'] = request.GET.get('menu_id')
                
                if int(request.GET.get('menu_id')) > Menu.objects.count():
                    return JsonResponse({"error_code" : "DOES_NOT_EXISTS_MENU"}, status = 404)
            if 'type_id' in request.GET.keys():
                filter_dict['productcategory__category__type_name'] = request.GET.get('type_id')
            products = Product.objects.prefetch_related(
                'productcategory_set__category'
            ).filter(**filter_dict).distinct().prefetch_related(
                'producttag_set__tag').prefetch_related('image_set')
            if search:
                products = products.filter(name_ko__contains = search)
            
            if sort == 'high_price':
                products = products.order_by('-price')
           
            elif sort == 'low_price':
                products = products.order_by('price')
            
            elif sort == 'new':
                products = products.order_by('id')
            product_list = [{
                'product_id'      : product.id,
                'product_name_ko' : product.name_ko,
                'product_tag'     : [tag_name.tag.name for tag_name in product.producttag_set.all()],
                'product_image'   : product.image_set.get(is_main_img=True).image_url
            } for product in products[offset : offset + limit]]
            return JsonResponse({"product_list" : product_list}, status = 200)
        except KeyError:
            return HttpResponse(status = 400)
    
class ProductDetailView(View):
    def get(self, request, product_id):
        try:

            if not product_id:
                raise KeyError

            if not Product.objects.filter(id = product_id).exists():
                return HttpResponse(status = 404)

            product = Product.objects.prefetch_related(
                'producttag_set__tag',
                'image_set',
                'productseries_set__series'
            ).get(id=product_id)

            series_id = None

            if product.productseries_set.filter(product_id=product_id).exists():
                series_id = product.productseries_set.get(product_id=product_id).series_id

            series = ProductSeries.objects.filter(series_id = series_id).prefetch_related('product__image_set')

            item = {
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
            
            if not item['product_series']:
                del item['product_series']

            return JsonResponse({"item" : item}, status = 200)

        except KeyError:
            return HttpResponse(status = 400)
