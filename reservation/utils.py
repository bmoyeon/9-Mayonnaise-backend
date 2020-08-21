import string
import random

from .models import Reservation

def check(num):
    if Reservation.objects.filter(reservation_number = num):
        return num

def create_num():
    string_num = string.ascii_letters + string.digits
    serial_num= ''.join(random.choice(string_num) for count in range(10))
    if check(serial_num):
        return create_num()
    return serial_num
