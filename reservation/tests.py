import json
import bcrypt
import jwt

from django.test import (
    TestCase, 
    Client
)

from .models import Reservation
from account.models import (
    Account,
    Gender
)

class ReservationCreateTest(TestCase):
    
    def setUp(self):
        Gender(
            id   = 1,
            name = "male"
        ).save()

        Account(
            id = 1,
            name            = "박준모",
            password        = bcrypt.hashpw('p1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthdate       = "19880705",
            gender          = Gender.objects.get(name="male"),
            phone_number    = "01041737335",
            user_email      = "junnoli18@gmail.com"
        ).save()

        Reservation.objects.create(
            reservation_number = "123",
            store              = "명동점",
            date               = "2020-07-20",
            time               = "5:30 PM",
            age                = "30~33세",
            account_id         = 1
        )

    def tearDown(self):
        Account.objects.all().delete()
        Gender.objects.all().delete()
        Reservation.objects.all().delete()
    
    def test_reservation_get_success(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        response = client.get('/reservation', content_type = 'application/json')
        result = {
            "user_info": {
                "user_name"         : "박준모",
                "user_phone_number" : "01041737335",
                "user_gender"       : "male"
            }
        }

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_reservation_get_fail(self):
        client   = Client(HTTP_Authorization="eyJ0eX")
        response = client.get('/reservation', content_type = 'application/json')

        self.assertEqual(response.json(), {"error_code" : "INVALID_TOKEN"})
        self.assertEqual(response.status_code, 401)
    
    def test_reservation_get_keyerror(self):
        client   = Client(HTTP_Authorizatio="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        response = client.get('/reservation', content_type = 'application/json')

        self.assertEqual(response.json(), {"error_code" : "INVALID_LOGIN"})
        self.assertEqual(response.status_code, 401)
    
    def test_reservstion_post_success(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        data_input = {
            "age"   : "20세",
            "time"  : "5:30 PM",
            "store" : "명동점",
            "date"  : "2020-07-12"
        }
        response = client.post('/reservation', json.dumps(data_input), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 200)
    
    def test_reservation_post_fail(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        data_input = {
            "age"   : "20세",
            "time"  : "5:30 PM",
            "store" : "명동점",
            "date"  : "2020-07-20"
        }
        response = client.post('/reservation', json.dumps(data_input), content_type = 'application/json')
        
        self.assertEqual(response.json(), {"error_code" : "ALREADY_EXISTS"})
        self.assertEqual(response.status_code, 401)
    
    def test_reservation_post_keyerror(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        data_input = {
            ""      : "20세",
            "time"  : "4:30 PM",
            "store" : "명동점",
            "date"  : "2020-07-12"
        }
        response = client.post('/reservation', json.dumps(data_input), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
    
    def test_reservation_delete_success(self):
        client = Client()
        response = client.delete('/reservation?reservation_no=123', content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
    
    def test_reservation_delete_fail(self):
        client = Client()
        response = client.delete('/reservation?reservation_no=456', content_type = 'application/json')

        self.assertEqual(response.json(), {"error_code" : "INVALID_RESERVATION_NO"})
        self.assertEqual(response.status_code, 401)
    
    def test_reservation_delete_keyerror(self):
        client = Client()
        response = client.delete('/reservation?reservation_n=123', content_type = 'application/json')

        self.assertEqual(response.status_code, 400)

class ReservationCheckTest(TestCase):

    def setUp(self):
        Gender(
            id   = 1,
            name = "male"
        ).save()

        Account(
            id = 1,
            name            = "박준모",
            password        = bcrypt.hashpw('p1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthdate       = "19880705",
            gender          = Gender.objects.get(name="male"),
            phone_number    = "01041737335",
            user_email      = "junnoli18@gmail.com"
        ).save()

        Reservation.objects.create(
            reservation_number = "123",
            store              = "명동점",
            date               = "2020-07-20",
            time               = "5:30 PM",
            age                = "30~33세",
            account_id         = 1
        )


    def tearDown(self):
        Account.objects.all().delete()
        Gender.objects.all().delete()
        Reservation.objects.all().delete()

    def test_reservation_check_get_success(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        response = client.get('/reservation/check', content_type = 'application/json')
        result = {
            "reservation_list": [
                {
                    "reservation_no": "123",
                    "reservation_store": "명동점",
                    "reservation_date": "2020-07-20",
                    "reservation_time": "5:30 PM",
                    "name": "박준모",
                    "phone_number": "01041737335"
                }
            ]
        }

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)
    
    def test_reservation_check_get_fail(self):
        client = Client(HTTP_Authorization="e0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        response = client.get('/reservation/check', content_type = 'application/json')

        self.assertEqual(response.json(), {"error_code" : "INVALID_TOKEN"})
        self.assertEqual(response.status_code, 401)
    
    def test_reservation_check_get_keyerror(self):
        client = Client(HTTP_Authorizatio="e0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        response = client.get('/reservation/check', content_type = 'application/json')

        self.assertEqual(response.json(), {"error_code" : "INVALID_LOGIN"})
        self.assertEqual(response.status_code, 401)
    
class ReservationUpdateTest(TestCase):
    def setUp(self):
        Gender(
            id   = 1,
            name = "male"
        ).save()

        Account(
            id = 1,
            name            = "박준모",
            password        = bcrypt.hashpw('p1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthdate       = "19880705",
            gender          = Gender.objects.get(name="male"),
            phone_number    = "01041737335",
            user_email      = "junnoli18@gmail.com"
        ).save()

        Reservation.objects.create(
            reservation_number = "123",
            store              = "명동점",
            date               = "2020-07-20",
            time               = "5:30 PM",
            age                = "30~33세",
            account_id         = 1
        )

    def tearDown(self):
        Account.objects.all().delete()
        Gender.objects.all().delete()
        Reservation.objects.all().delete()
    
    def test_reservation_update_get_success(self):
        client = Client()
        response = client.get('/reservation/update?reservation_no=123', content_type = 'application/json')
        result = {
            "reservation_info": {
                "reservation_no": "123",
                "reservation_store": "명동점",
                "reservation_date": "2020-07-20",
                "reservation_time": "5:30 PM",
                "name": "박준모",
                "phone_number": "01041737335"
            }
        }

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)
    
    def test_reservation_update_get_fail(self):
        client = Client()
        response = client.get('/reservation/update?reservation_no=789', content_type = 'application/json')

        self.assertEqual(response.json(), {"error_code" : "INVALID_RESERVATION_NO"})
        self.assertEqual(response.status_code, 401)

    def test_reservation_update_get_keyerror(self):
        client = Client()
        response = client.get('/reservation/update', content_type = 'application/json')

        self.assertEqual(response.status_code, 400)

    def test_reservation_update_put_success(self):
        client = Client()
        data_input = {
            "age"   : "20세",
            "time"  : "5:30 PM",
            "store" : "명동점",
            "date"  : "2020-07-12"
        }
        response = client.put('/reservation/update?reservation_no=123', json.dumps(data_input), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
    
    def test_reservation_update_put_fail(self):
        client = Client()
        response = client.get('/reservation/update?reservation_no=789', content_type = 'application/json')

        self.assertEqual(response.json(), {"error_code" : "INVALID_RESERVATION_NO"})
        self.assertEqual(response.status_code, 401)
    
    def test_reservation_update_put_keyerror(self):
        client = Client(HTTP_Authorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ")
        data_input = {
            ""      : "20세",
            "time"  : "4:30 PM",
            "store" : "명동점",
            "date"  : "2020-07-12"
        }
        response = client.post('/reservation', json.dumps(data_input), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)