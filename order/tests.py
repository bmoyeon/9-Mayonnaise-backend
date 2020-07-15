import json
import re
import bcrypt
import jwt
import unittest

from django.test       import TestCase
from django.test       import Client
from unittest.mock     import (
    patch, 
    MagicMock
)

from account.models     import (
    Account,
    Gender
)
from product.models     import Product
from .models            import *

class CartTest(TestCase):
    def setUp(self):  
        Gender(
            id      =   1,
            name    = "male"
            ).save()
        
        Account(
            id =1,
            name            = "박준모",
            password        = bcrypt.hashpw('p1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthdate       = "19880705",
            gender          = Gender.objects.get(name="male"),
            phone_number    = "01041737335",
            user_email      = "junnoli18@gmail.com"
        ).save()
        
        Product(
            id              =    1,
            name_ko         = "워터뱅크 모이스춰 에센스",
            name_en         = "Water Bank Moisture Essence",
            description     = "산뜻하게 수분을 충전해주는 워터리 텍스쳐로 강력하게 자외선을 차단해주는 수분 선크림이에요",
            price           = "40000",
            volume          = "70ml",
            ingredient      = "junnoli18@gmail.com",
            feature         = "junnoli18@gmail.com"
        ).save()
        
        OrderStatus(
            id      = 1,
            name    = "장바구니"    
        ).save()
        
        Order(
            id =1,
            account         = Account.objects.get(id="1"),
            status          = OrderStatus.objects.get(id="1")    
        ).save()
        
        OrderProduct(
            id =1,
            order            = Order.objects.get(id="1"),
            product          = Product.objects.get(id="1"),
            price            = "20000"       
        ).save()
             
    def tearDown(self):
        Account.objects.all().delete()
        Gender.objects.all().delete()
        Product.objects.all().delete()
        OrderStatus.objects.all().delete()
        Order.objects.all().delete()
        OrderProduct.objects.all().delete()
        
    def test_cart_add_success(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")

        order = {
            "id"             : 1,
            "account_id"     : 1,
            "status"         : 1
        }
        
        orderproduct = {
            "product"   : 1,
            "quantity"  : 1,
            "price"     : 20000,
            "order"     : 1
        }
        
        data = {
            "order"         : order,
            "product"       : 1,
            "quantity"      : 1,
            "orderproduct"  : orderproduct
            }
        
        response = client.post("/order/cart",json.dumps(data), content_type = "application/json")
        self.assertEqual(response.status_code, 200)
       
    def test_cart_add_key_error(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")

        order = {
            "id"            :1,
            "account_id"    : 1,
            "status"        : 1
        }
        
        orderproduct = {
            "product"   : 1,
            "quantity"  : 1,
            "price"     : 20000,
            "orders"    : 1
        }
        
        data = {
            "order"         : order,
            "products"      : 1,
            "quantity"      : 1, 
            "orderproduct"  : orderproduct
            }
        
        response = client.post("/order/cart",json.dumps(data), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "INVALID_KEYS"})
        
    def test_cart_add_token_error(self):
        client = Client()

        order = {
            "id"            :1,
            "account_id"    : 1,
            "status"        : 1
        }
        
        orderproduct = {
            "product"   : 1,
            "quantity"  : 1,
            "price"     : 20000,
            "order"    : 1
        }
        
        data = {
            "order"         : order,
            "product"      : 1,
            "quantity"      : 1, 
            "orderproduct"  : orderproduct
            }
        
        response = client.post("/order/cart",json.dumps(data), content_type = "application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "INVALID_LOGIN"})
        