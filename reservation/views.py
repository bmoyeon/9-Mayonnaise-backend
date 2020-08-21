import json
import random

from django.views import View
from django.http  import (
    JsonResponse,
    HttpResponse
)

from .models import Reservation
from .utils import (
    check,
    create_num
)
from account.models import Account
from account.utils import login_required

class ReservationView(View):

    @login_required
    def get(self, request):
        user = Account.objects.select_related('gender').get(id = request.user.id)
        user_info = {
            'user_name'   : request.user.name,
            'user_phone'  : request.user.phone,
            'user_gender' : user.gender.name
        }
        return JsonResponse({'user_info' : user_info}, status = 200)

    @login_required
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Reservation.objects.filter(date = data['date'], time = data['time']).exists():
                return JsonResponse({'message' : 'ALREADY_EXISTS'}, status = 401)

            serial_number = create_num()
            Reservation.objects.create(
                reservation_number = serial_number,
                store              = data['store'],
                date               = data['date'],
                time               = data['time'],
                age                = data['age'],
                account            = request.user
            )
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

    def delete(self, request):
        try:
            if 'reservation_no' not in request.GET.keys():
                raise KeyError
            reservation_no = request.GET.get('reservation_no')

            if not Reservation.objects.filter(reservation_number = reservation_no).exists():
                return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status = 401)

            reservation = Reservation.objects.get(reservation_number = reservation_no)
            reservation.delete()
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class ReservationCheckView(View):
    @login_required
    def get(self, request):
        try:
            account_id = request.user.id
            reservations = Reservation.objects.filter(account = account_id).select_related(
                'account').order_by('-created_at')

            reservation_list = [{
                "reservation_no"    : reservation.reservation_number,
                "reservation_store" : reservation.store,
                "reservation_date"  : reservation.date,
                "reservation_time"  : reservation.time,
                "name"              : reservation.account.name,
                "phone"             : reservation.account.phone
            } for reservation in reservations]
            return JsonResponse({"reservation_list" : reservation_list}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class ReservationUpdateView(View):
    def get(self, request):
        try:
            if 'reservation_no' not in request.GET.keys():
                raise KeyError
            reservation_no = request.GET.get('reservation_no')

            if not Reservation.objects.filter(reservation_number = reservation_no).exists():
                return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status = 401)

            reservation = Reservation.objects.get(reservation_number = reservation_no)
            reservation_info = {
                "reservation_no"    : reservation.reservation_number,
                "reservation_store" : reservation.store,
                "reservation_date"  : reservation.date,
                "reservation_time"  : reservation.time,
                "name"              : reservation.account.name,
                "phone"             : reservation.account.phone
            }
            return JsonResponse({"reservation_info" : reservation_info}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

    def put(self, request):
        data = json.loads(request.body)

        try:
            reservation_no = request.GET.get('reservation_no', None)

            if not Reservation.objects.filter(reservation_number = reservation_no).exists():
                return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status = 401)

            reservation = Reservation.objects.get(reservation_number = reservation_no)
            reservation.store = data['store']
            reservation.date  = data['date']
            reservation.time  = data['time']
            reservation.age   = data['age']

            reservation.save()
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
