import json
import bcrypt
import jwt
import requests
import hashlib
import hmac
import base64
import time

from laneige.settings        import (
    SECRET_KEY,
    ACCESS_KEY,
    NAVER_SECRET_KEY,
    NAVER_SMS_URI,
    NAVER_URI,
    ALGORITHM
)

from django.db import transaction
from django.views import View
from django.http  import (
    JsonResponse, 
    HttpResponse
)

from .models    import (
    Order, 
    OrderProduct, 
    OrderStatus
)

from product.models  import Product,Image
from account.models  import Account
from account.utils   import login_required

class CartAddView(View):
    @login_required
    def post(self, request):
        cart_data = json.loads(request.body)
        
        try :
            
            product = Product.objects.get(id = cart_data['product'])
          
            order = Order.objects.create(
                account = Account.objects.get(id=request.user_id),
                status  = OrderStatus.objects.get(name="장바구니")
                )
            
            OrderProduct.objects.create(
                product    = Product.objects.get(id=cart_data['product']),
                quantity   = cart_data['quantity'],
                price      = product.price,
                order      = order
                )
                
            return HttpResponse(status = 200)
            
        except KeyError:    
            return JsonResponse({ 'message' : 'INVALID_KEYS'}, status=400)

class CartListView(View):
    @login_required
    def get(self, request):
        try :
            products = Product.objects.prefetch_related(
                    'orderproduct_set',
                    'orderproduct_set__order',
                    'image_set'
                ).filter(orderproduct__order__account=request.user_id,orderproduct__order__status=1)
            
            product_list = [{
                'cart_num'          : product.orderproduct_set.first().id,
                'productNum'        : product.id,
                'productKoName'     : product.name_ko,
                'productEnName'     : product.name_en,
                'productImg'        : product.image_set.get(is_main_img=True, product=product.id).image_url,
                'productVolumn'     : product.volume,
                'productPrice'      : product.price,
                'productQuantity'   : 1,
            } for product in products]
        
            return JsonResponse({"product_list" : product_list}, status = 200)
        
        except : 
            return JsonResponse({"message" : "EMPTY_CART"}, status = 400)

    @login_required
    def put(self, request):
        data = json.loads(request.body)
        try :    
            cart = OrderProduct.objects.get(order__account=request.user_id,id=data['cart_num'])  
            cart.quantity =data['quantity']
            cart.update()

            products = OrderProduct.objects.select_related('order', 'product').filter(order__account=request.user_id,order__status=1)
            product_list = [{
                'cart_num'          : product.id,
                'productNum'        : product.product.id,
                'productKoName'     : product.product.name_ko,
                'productEnName'     : product.product.name_en,
                'productImg'        : Image.objects.get(is_main_img=True, product=product.product.id).image_url,
                'productVolumn'     : product.product.volume,
                'productPrice'      : product.product.price,
                'productQuantity'   : product.quantity
            } for product in products]
            
            return JsonResponse({"product_list" : product_list}, status = 200)
        
        except :
            return JsonResponse({"message" : "NOT_EXIST_CART_NUMBER"}, status = 400)
        
    @login_required
    def delete(self, request):
        try :
            data = json.loads(request.body)
            cart = OrderProduct.objects.get(order__account=request.user_id,id=data['cart_num'])  
            cart.delete()

            products = OrderProduct.objects.select_related('order', 'product').filter(order__account=request.user_id,order__status=1)
            product_list = [{
                'cart_num'          : product.id,
                'productNum'        : product.product.id,
                'productKoName'     : product.product.name_ko,
                'productEnName'     : product.product.name_en,
                'productImg'        : Image.objects.get(is_main_img=True, product=product.product.id).image_url,
                'productVolumn'     : product.product.volume,
                'productPrice'      : product.product.price,
                'productQuantity'   : product.quantity
            } for product in products]
            
            return JsonResponse({"product_list" : product_list}, status = 200)
        
        except :
            return JsonResponse({"product_list" :"NOT_EXIST_CART_NUMBER"}, status = 200)   
        
