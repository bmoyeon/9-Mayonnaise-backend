import json
import random
import string

from django.views import View
from django.http  import (
    JsonResponse,
    HttpResponse
)

from .models        import Reservation
from account.models import Account
from account.utils  import (
    login_required,
    send_sms_reservation
)

class ReservationView(View):

    @login_required
    def get(self, request):
        user = Account.objects.select_related('gender').get(id = request.user_id.id)
        user_info = {
            'user_name'         : request.user_id.name,
            'user_phone_number' : request.user_id.phone_number,
            'user_gender'       : user.gender.name
        }
        return JsonResponse({'user_info' : user_info}, status = 200)
    
    @login_required
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Reservation.objects.filter(date = data['date'], time = data['time']).exists():
                return JsonResponse({"error_code" : 'ALREADY_EXISTS'}, status = 401)

            def check(num):
                if Reservation.objects.filter(reservation_number = num):
                    return num
                
            def create_num():
                string_num = string.ascii_letters + string.digits
                serial_num= ''.join(random.choice(string_num) for i in range(10))
                if check(serial_num):  
                    return create_num()
                return serial_num

            serial_number = create_num()

            Reservation.objects.create(
                reservation_number = serial_number,
                store              = data['store'],
                date               = data['date'],
                time               = data['time'],
                age                = data['age'],
                account            = request.user_id
            )

            send_sms_reservation(
                u_phone = request.user_id.phone_number,
                u_name = request.user_id.name,
                u_number = serial_number,
                date = data['date'],
                time = data['time'],
                store = data['store']
            )
            
            return HttpResponse(status = 200)

        except KeyError:
            return HttpResponse(status = 400)
    
    def delete(self, request):
        reservation_no = request.GET.get('reservation_no')

        try:
            if 'reservation_no' not in request.GET.keys():
                raise KeyError

            if not Reservation.objects.filter(reservation_number = reservation_no).exists():
                return JsonResponse({"error_code" : "INVALID_RESERVATION_NO"}, status = 401)
            
            reservation = Reservation.objects.get(reservation_number = reservation_no)
            reservation.delete()
            return HttpResponse(status = 200)
        
        except KeyError:
            return HttpResponse(status = 400)

class ReservationCheckView(View):
    @login_required
    def get(self, request):
        try:
            account_id = request.user_id
            reservation_all = Reservation.objects.select_related('account').filter(
                account_id = account_id).order_by('-created_at')

            reservation_list = [{
                "reservation_no"     : reservation.reservation_number,
                "reservation_store"  : reservation.store,
                "reservation_date"   : reservation.date,
                "reservation_time"   : reservation.time,
                "name"               : reservation.account.name,
                "phone_number"       : reservation.account.phone_number
            } for reservation in reservation_all]
            return JsonResponse({"reservation_list" : reservation_list}, status = 200)

        except KeyError:
            return HttpResponse(status = 400)

class ReservationUpdateView(View):
    def get(self, request):
        reservation_no = request.GET.get('reservation_no')

        try:
            if 'reservation_no' not in request.GET.keys():
                raise KeyError

            if not Reservation.objects.filter(reservation_number = reservation_no).exists():
                    return JsonResponse({"error_code" : "INVALID_RESERVATION_NO"}, status = 401)
        
            reservation = Reservation.objects.get(reservation_number = reservation_no)
            reservation_info = {
                "reservation_no"     : reservation.reservation_number,
                "reservation_store"  : reservation.store,
                "reservation_date"   : reservation.date,
                "reservation_time"   : reservation.time,
                "name"               : reservation.account.name,
                "phone_number"       : reservation.account.phone_number
            }
            return JsonResponse({"reservation_info" : reservation_info}, status = 200)
        
        except KeyError:
            return HttpResponse(status = 400)

    def put(self, request):
        data = json.loads(request.body)
        try:
            reservation_no = request.GET.get('reservation_no')

            if not Reservation.objects.filter(reservation_number = reservation_no).exists():
                return JsonResponse({"error_code" : "INVALID_RESERVATION_NO"}, status = 401)

            reservation = Reservation.objects.get(reservation_number = reservation_no)
            reservation.store = data['store']
            reservation.date  = data['date']
            reservation.time  = data['time']
            reservation.age   = data['age']

            reservation.save()
            return HttpResponse(status = 200)

        except KeyError:
            return HttpResponse(status = 400)