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

from .models     import (
    Account,
    Gender
)

class SignUpTest(TestCase):
    def setUp(self):  
        Gender(
            id =1,
            name = "male"
            ).save()
        
        Account(
            name            = "박준모",
            password        = bcrypt.hashpw('p1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthdate       = "19880705",
            gender          = Gender.objects.get(name="male"),
            phone_number    = "01041737335",
            user_email      = "junnoli18@gmail.com"
        ).save()

    def tearDown(self):
        Account.objects.all().delete()
        Gender.objects.all().delete()
    
    def test_signup_success(self):
        client = Client()
        account = {
            "name"            : "박준모",
            "password"        : "p1234",
            "birthdate"       : "19330303",
            "gender"          : "male",
            "phone_number"    : "01029394858",
            "user_email"      : "junnoli1@naver.com"
        }
        
        response = client.post("/account/sign-up", json.dumps(account), content_type = "application/json")
        self.assertEqual(response.status_code, 200)
        
    def test_signup_exists_email(self):
        client = Client()
        account = {
            "name"            : "박준모",
            "password"        : "p1234",
            "birthdate"       : "19330303",
            "gender"          : "male",
            "phone_number"    : "01029394858",
            "user_email"      : "junnoli18@gmail.com"
        }

        response = client.post("/account/sign-up", json.dumps(account), content_type = "application/json")
        self.assertEqual(response.status_code, 400)   
        self.assertEqual(response.json(), {"message" : "ALREADY_EXISTS"})
        
    def test_signup_key_error(self):
        client = Client()
        account = {
            "id"              : "박준모",
            "password"        : "p1234",
            "birthdate"       : "19330303",
            "gender"          : "male",
            "phone_number"    : "01029394858",
            "user_email"      : "junnoli111@gmail.com"
        }

        response = client.post("/account/sign-up", json.dumps(account), content_type = "application/json")
        self.assertEqual(response.status_code, 400)   
        self.assertEqual(response.json(), {"message" : "INVALID_KEYS"})    
    
class SignInTest(TestCase):
    def setUp(self):
        Gender(
            id =1,
            name = "male"
            ).save()
        
        Account(
            name            = "박준모",
            password        = bcrypt.hashpw('p1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthdate       = "19880705",
            gender          = Gender.objects.get(name="male"),
            phone_number    = "01041737335",
            user_email      = "junnoli18@gmail.com"
        ).save()

    def tearDown(self):
        Account.objects.all().delete()
        Gender.objects.all().delete()        
    
    def test_signin_success(self): 
        client = Client()
        account = {
            "password"        : "p1234",
            "user_email"      : "junnoli18@gmail.com"
        }
        
        response = client.post("/account/sign-in", json.dumps(account), content_type = "application/json")
        self.assertEqual(response.status_code, 200)
    
    def test_signin_wrong_password(self):
        client = Client()
        account = {
            "password"        : "p12345",
            "user_email"      : "junnoli18@gmail.com"
        }
        
        response = client.post("/account/sign-in", json.dumps(account), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "WRONG_PASSWORD"}) 
        
    def test_signin_not_exist_email(self):
        client = Client()
        account = {
            "password"        : "p1234",
            "user_email"      : "junnoli20@gmail.com"
        }
        
        response = client.post("/account/sign-in", json.dumps(account), content_type = "application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message" : "NOT_EXIST_EMAIL"}) 
        
    def test_signin_key_error(self):
        client = Client()
        account = {
            "password"        : "p1234",
            "user_id"         : "junnoli20@gmail.com"
        }
        
        response = client.post("/account/sign-in", json.dumps(account), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "INVALID_KEYS"})
        
class KakaoLoginTest(TestCase):
    def setUp(self):
        Gender(
            id =1,
            name = "male"
            ).save()
        
        Account(
            name            = "박준모",
            password        = bcrypt.hashpw('p1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthdate       = "19880705",
            gender          = Gender.objects.get(name="male"),
            phone_number    = "01041737335",
            user_email      = "junnoli18@gmail.com"
        ).save()
    
    @patch('account.views.requests')
    def test_kakao_signin_success(self, mocked_request):
        class FakeResponse:
            def json(self):
                return {
                    "id"            : 12345,
                    "properties"    : {"nickname": "test_user"},
                    "kakao_account" : {"email":"test@gmail.com","gender":"male","birthday":"18000908"}
                }
        mocked_request.get = MagicMock(return_value = FakeResponse())
        
        client = Client()
        header = {'HTTP_Authorization':'fake_token.1234'}
        response = client.post('/account/kakao-login', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)
        
    @patch('account.views.requests')
    def test_kakao_signin_keyerror(self, mocked_request):
        class FakeResponse:
            def json(self):
                return {
                    "id" : 12345,
                    "properties"    : {"username": "test_user"},
                    "kakao_account" : {"email":"test@gmail.com","gender":"male","birthday":"18000908"}
                }
        mocked_request.get = MagicMock(return_value = FakeResponse())
        
        client = Client()
        header = {'HTTP_Authorization':'fake_token.1234'}
        response = client.post('/account/kakao-login', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()

        

 
        


    