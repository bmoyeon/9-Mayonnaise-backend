import json
import jwt
import bcrypt
import re
import requests

from django.views           import View
from django.core.exceptions import ValidationError
from django.http            import (
    JsonResponse,
    HttpResponse
)

from laneige.settings        import (
    SECRET_KEY,
    ACCESS_KEY,
    NAVER_SECRET_KEY,
    NAVER_SMS_URI,
    NAVER_URI,
    ALGORITHM
)

from .models                import (
    Account,
    Gender
)
from .utils  import send_sms

class SignUpView(View):
    def post(self, request):
        account_data = json.loads(request.body)
        
        try:
            if Account.objects.filter(user_email=account_data['user_email']).exists():
                return JsonResponse({'message':'ALREADY_EXISTS'},status = 400)
            
            else :
                hashed_password = bcrypt.hashpw(account_data['password'].encode('utf-8'), bcrypt.gensalt())
                Account(
                    name            = account_data['name'],
                    password        = hashed_password.decode('utf-8'),
                    birthdate       = account_data['birthdate'],
                    gender          = Gender.objects.get(name=account_data['gender']),
                    phone_number    = account_data['phone_number'],
                    user_email      = account_data['user_email']
                ).save()
                
                send_sms(account_data['phone_number'])
                return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status = 400)
        
class SignInView(View):
    def post(self, request):
        account_data = json.loads(request.body)
        
        try:
            if Account.objects.filter(user_email=account_data['user_email']).exists():
                account = Account.objects.get(user_email=account_data['user_email'])
                
                if bcrypt.checkpw(account_data['password'].encode('utf-8'), account.password.encode('utf-8')):
                    token = jwt.encode({'user_id' : account.id }, SECRET_KEY, algorithm = ALGORITHM)
                    return JsonResponse({ 'access_token' : token.decode('utf-8')}, status=200)
                 
                return JsonResponse({ 'message' : 'WRONG_PASSWORD'}, status=400)    
            return JsonResponse({ 'message' : 'NOT_EXIST_EMAIL'}, status=401)

        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS'}, status=400)
        
class KakaoView(View):
    def post(self, request):
        access_token = request.headers['Authorization']

        kakao_request = requests.get(
            'https://kapi.kakao.com/v2/user/me',
            headers = {
                "Host"          : "kapi.kakao.com",
                "Authorization" : f"Bearer {access_token}",
                "Content-type"  : "application/x-www-from-urlencoded;charset=utf-8"
            }
        ,timeout = 2)
        
        kakao_id        = kakao_request.json().get('id')
        kakao_properties  = kakao_request.json().get('properties')
        kakao_account     = kakao_request.json().get('kakao_account')
        
        try:
            if Account.objects.filter(is_social_user = kakao_id).exists():
                user    = Account.objects.get(is_social_user = kakao_id)
                token   = jwt.encode({'user_id' : user.id }, SECRET_KEY, algorithm = ALGORITHM)
                return JsonResponse({"access_token":token.decode('utf-8')}, status = 200)

            else:
                Account(
                    is_social_user         = kakao_id,
                    gender                 = Gender.objects.get(name=kakao_account['gender']),
                    user_email             = kakao_account['email'],
                    name                   = kakao_properties['nickname'],
                    birthdate              = kakao_account['birthday']
                ).save()

                user    = Account.objects.get(is_social_user = kakao_id)
                token   = jwt.encode({'user_id' : user.id }, SECRET_KEY, algorithm = ALGORITHM)
                return JsonResponse({"access_token":token.decode('utf-8')}, status = 200)
                
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)


