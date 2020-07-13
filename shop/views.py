import json

from django.views           import View
from django.core.exceptions import ObjectDoesNotExist
from .models                import Shop
from django.http            import (
    JsonResponse, 
    HttpResponse
)

class shopListView(View):
    def get(self, request):
        try:
            if 'search' not in request.GET.keys():
                raise KeyError

            input_data          =       request.GET.get('search')
            search              =       {}
            
            if input_data:
                search          =       {'address__contains' : input_data}
            
            shop_list = Shop.objects.filter(**search)
            
            shops = [
                {
                    'shopName'      :       shops.name,
                    'address'       :       shops.address,
                    'contact'       :       shops.contact,
                    'latitude'      :       shops.latitude,
                    'longitude'     :       shops.longitude
                }
                for shops in shop_list
            ]

            return JsonResponse({"shops":shops} , status = 200)

        except KeyError:
            return HttpResponse(status = 400)