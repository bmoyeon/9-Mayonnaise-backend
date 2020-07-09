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
    Product
)

class ProductListView(View):
    def get(self, request):        
        try:
            if 'menu_id' not in request.GET.keys():
                raise KeyError

            if not Menu.objects.filter(id = request.GET.get('menu_id')).exists():
                return HttpResponse(status = 404)

            filter_dict = {
                'productcategory__category__menu'      : request.GET.get('menu_id'), 
                'productcategory__category__type_name' : request.GET.get('type_id')
            }
            
            if 'type_id' not in request.GET.keys():
                del filter_dict['productcategory__category__type_name']

            products = Product.objects.prefetch_related(
                'productcategory_set__category'
            ).filter(**filter_dict).distinct().prefetch_related(
                'producttag_set__tag').prefetch_related('image_set')

            product_list = [{
                'product_id'      : product.id,
                'product_name_ko' : product.name_ko,
                'product_tag'     : [tag_name.tag.name for tag_name in product.producttag_set.all()],
                'product_image'   : product.image_set.get(is_main_img=True).image_url
            } for product in products]

            return JsonResponse({"product_list" : product_list}, status = 200)

        except KeyError:
            return HttpResponse(status = 400)