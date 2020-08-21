import json
import jwt
import bcrypt

from django.views import View
from django.http import (
    JsonResponse,
    HttpResponse
)

from laneige.settings import (
    SECRET_KEY,
    ALGORITHM
)
from .models import (
    Account,
    Gender
)

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'ALREADY_EXISTS'}, status = 401)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            Account.objects.create(
                name     = data['name'],
                emial    = data['email'],
                password = hashed_password.decode('utf-8'),
                phone    = data['phone_number'],
                gender   = Gender.objects.get(name = data['gender'])
            )
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(email = data['email']).exists():
                user = Account.objects.get(email = data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'id' : user.id }, SECRET_KEY, algorithm = ALGORITHM)
                    return JsonResponse({'access_token' : access_token.decode('utf-8')}, status = 200)

                return JsonResponse({'message' : 'UNAUTHORIZED'}, status = 401)
            return JsonResponse({'message' : 'UNAUTHORIZED'}, status = 401)

        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS'}, status=400)
