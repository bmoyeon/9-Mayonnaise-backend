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

class CartAddTest(TestCase):
    def setUp(self):  
        Gender(
            id      =   1,
            name    = "male"
            ).save()
        
        Account(
            id =1,
            name            = "홍길동",
            password        = bcrypt.hashpw('p1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthdate       = "19880705",
            gender          = Gender.objects.get(name="male"),
            phone_number    = "01012345678",
            user_email      = "test@gmail.com"
        ).save()
        
        Product(
            id              =    1,
            name_ko         = "워터뱅크 모이스춰 에센스",
            name_en         = "Water Bank Moisture Essence",
            description     = "산뜻하게 수분을 충전해주는 워터리 텍스쳐로 강력하게 자외선을 차단해주는 수분 선크림이에요",
            price           = "40000",
            volume          = "70ml",
            ingredient      = "전성분,물,소금",
            feature         = "전성분,물,소금"
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
        
    def test_cart_add_invalid_login_error(self):
        client = Client()
        
        response = client.post("/order/cart",content_type = "application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "INVALID_LOGIN"})

    def test_cart_add_invalid_login_error(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGcOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        
        response = client.post("/order/cart",content_type = "application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "INVALID_TOKEN"})
    
    def test_cart_add_unknown_user_error(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2fQ.xuue7ava7EckJ7cvT2bEIHHXsYAizRSZNR6kJBAC22c")
        
        response = client.post("/order/cart",content_type = "application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "UNKNOWN_USER"})

class CartListTest(TestCase):
    def setUp(self):  
        Gender(
            id      =   1,
            name    = "male"
            ).save()
        
        Account(
            id =1,
            name            = "홍길동",
            password        = bcrypt.hashpw('p1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthdate       = "19880705",
            gender          = Gender.objects.get(name="male"),
            phone_number    = "01012345678",
            user_email      = "test@gmail.com"
        ).save()
        
        Product(
            id              = 1,
            name_ko         = "워터뱅크 모이스춰 에센스",
            name_en         = "Water Bank Moisture Essence",
            description     = "산뜻하게 수분을 충전해주는 워터리 텍스쳐로 강력하게 자외선을 차단해주는 수분 선크림이에요",
            price           = "40000",
            volume          = "70ml",
            ingredient      = "전성분,물,소금",
            feature         = "전성분,물,소금"
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
            price            = "20000",
            quantity         = 1
                   
        ).save()
        
        Image(
            id=1,
            image_url ="https://www.laneige.com/kr/ko/skincare/__icsFiles/afieldfile/2020/03/10/wd-emulsion-02_1.png",
            product = Product.objects.get(id="1"),
            is_main_img = "1"
        ).save()
             
    def tearDown(self):
        Account.objects.all().delete()
        Gender.objects.all().delete()
        Product.objects.all().delete()
        OrderStatus.objects.all().delete()
        Order.objects.all().delete()
        OrderProduct.objects.all().delete()
        Image.objects.all().delete()
               
    def test_show_cartlist_success(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        response = client.get('/order/cartlist', content_type = 'application/json')
        
        result = {
        "product_list": [
                {
                "cart_num": 1,
                "productNum": 1,
                "productKoName": "워터뱅크 모이스춰 에센스",
                "productEnName": "Water Bank Moisture Essence",
                "productImg": "https://www.laneige.com/kr/ko/skincare/__icsFiles/afieldfile/2020/03/10/wd-emulsion-02_1.png",
                "productVolumn": "70ml",
                "productPrice": 40000,
                "productQuantity" :1
                }
            ]
        }
        
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)
    
    def test_show_cartlist_invaild_login_error(self):
        client = Client()
        response = client.get('/order/cartlist', content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "INVALID_LOGIN"})
        
    def test_show_cartlist_invaild_token_error(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewnQ")
        response = client.get('/order/cartlist', content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "INVALID_TOKEN"})
        
    def test_show_cartlist_unknown_user_error(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2fQ.xuue7ava7EckJ7cvT2bEIHHXsYAizRSZNR6kJBAC22c")
        response = client.get('/order/cartlist', content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "UNKNOWN_USER"})
    
    def test_update_cartlist_success(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        data = {
            "cart_num"     : 1,
            "quantity"     : 3 
            }
        
        response = client.put('/order/cartlist',json.dumps(data), content_type = 'application/json')
        
        result = {
        "product_list": [
                {
                "cart_num": 1,
                "productNum": 1,
                "productKoName": "워터뱅크 모이스춰 에센스",
                "productEnName": "Water Bank Moisture Essence",
                "productImg": "https://www.laneige.com/kr/ko/skincare/__icsFiles/afieldfile/2020/03/10/wd-emulsion-02_1.png",
                "productVolumn": "70ml",
                "productPrice": 40000,
                "productQuantity" :3
                }
            ]
        }
        
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)   
        
    def test_update_cartlist_invalid_token_error(self):
        client = Client()
        response = client.put('/order/cartlist', content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "INVALID_LOGIN"}) 
    
    def test_update_cartlist_invaild_token_error(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewnQ")
        response = client.put('/order/cartlist', content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "INVALID_TOKEN"})
        
    def test_update_cartlist_unknown_user_error(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2fQ.xuue7ava7EckJ7cvT2bEIHHXsYAizRSZNR6kJBAC22c")
        response = client.put('/order/cartlist', content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "UNKNOWN_USER"})   
    
    def test_delete_cartlist_success(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        data = {
            "cart_num"     : 1,
            }
        
        response = client.delete('/order/cartlist',json.dumps(data), content_type = 'application/json')
        
        result = {
        "product_list": []
        }
        
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)  
        
    def test_delete_cartlist_token_error(self):
        client = Client()
        response = client.delete('/order/cartlist', content_type = 'application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "INVALID_LOGIN"})
    
    def test_delete_cartlist_invaild_token_error(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewnQ")
        response = client.delete('/order/cartlist', content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "INVALID_TOKEN"})
        
    def test_delete_cartlist_unknown_user_error(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2fQ.xuue7ava7EckJ7cvT2bEIHHXsYAizRSZNR6kJBAC22c")
        response = client.delete('/order/cartlist', content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error_code" : "UNKNOWN_USER"})  
