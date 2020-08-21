import json
import bcrypt
import jwt
import requests

from django.http import JsonResponse

from account.models import Account
from laneige.settings import (
    SECRET_KEY,
    ALGORITHM
)

def login_required(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            access_token = request.headers['Authorization']
            user_id = jwt.decode(access_token, SECRET_KEY, algorithm = ALGORITHM)['id']
            user = Account.objects.get(id = user_id)
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 400)

        except Account.DoesNotExist:
            return JsonResponse({'message' : 'UNKNOWN_USER'}, status = 401)

    return wrapper
