import json
import bcrypt
import jwt
import requests
import hashlib
import hmac
import base64
import time

from django.http import JsonResponse

from account.models import Account
from laneige.settings import (
    SECRET_KEY,
    ACCESS_KEY,
    NAVER_SECRET_KEY,
    NAVER_SMS_URI,
    NAVER_URI,
    ALGORITHM
)


def login_required(func):
    def wrapper(self, request=requests, *args, **kwargs):
        try:
            encode_token = request.headers["Authorization"]
            if "Authorization" not in request.headers:
                return JsonResponse({"error_code": "INVALID_LOGIN"}, status=401)
            data = jwt.decode(encode_token, SECRET_KEY, algorithms='HS256')
            user = Account.objects.get(id=data['user_id'])
            request.user_id = user
            return func(self, request, *args, **kwargs)
        except jwt.DecodeError:
            return JsonResponse({"error_code": "INVALID_TOKEN"}, status=401)
        except Account.DoesNotExist:
            return JsonResponse({"error_code": "UNKNOWN_USER"}, status=401)
        except Exception as e:
            print(e)

    return wrapper


def send_sms(phone_number):

    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    access_key = ACCESS_KEY
    secret_key = NAVER_SECRET_KEY
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    uri = NAVER_URI
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(
        hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }

    payload = {
        'type': 'SMS',
        'contentType': 'COMM',
                'countryCode': "82",
                'from': '01041727335',
                'messages': [{'to': phone_number}],
                'content': "라네즈 회원 가입을 축하합니다"
    }

    requests.post(NAVER_SMS_URI, headers=headers, json=payload)
