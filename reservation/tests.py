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
from laneige.settings import (
    SECRET_KEY,
    ALGORITHM
)

hashed_password = bcrypt.hashpw('p1234'.encode('utf-8'), bcrypt.gensalt())
access_token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')

class ReservationCreateTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id   = 1,
            name = "male"
        )

        Account.objects.create(
            id       = 1,
            name     = "user",
            password = hashed_password.decode('utf-8'),
            gender   = Gender.objects.get(id = 1),
            phone    = "123456789",
            email    = "bmo@gmail.com"
        )

        Reservation.objects.create(
            reservation_number = "123",
            store              = "명동점",
            date               = "2020-07-20",
            time               = "5:30 PM",
            age                = "20~25세",
            account            = Account.objects.get(id = 1)
        )

    def tearDown(self):
        Gender.objects.all().delete()
        Account.objects.all().delete()
        Reservation.objects.all().delete()

    def test_reservation_get_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : access_token}
        response = client.get('/reservation', **header, content_type = 'application/json')
        result = {
            "user_info": {
                "user_name"   : "user",
                "user_phone"  : "123456789",
                "user_gender" : "male"
            }
        }
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_reservation_get_fail(self):
        client   = Client()
        header = {'HTTP_AUTHORIZATION' : '1'}
        response = client.get('/reservation', **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'INVALID_TOKEN'})
        self.assertEqual(response.status_code, 400)

    def test_reservstion_post_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : access_token}
        data_input = {
            "age"   : "20세",
            "time"  : "5:30 PM",
            "store" : "명동점",
            "date"  : "2020-07-12"
        }
        response = client.post('/reservation', json.dumps(data_input), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_reservation_post_already_exists(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : access_token}
        data_input = {
            "age"   : "20세",
            "time"  : "5:30 PM",
            "store" : "명동점",
            "date"  : "2020-07-20"
        }
        response = client.post('/reservation', json.dumps(data_input), **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'ALREADY_EXISTS'})
        self.assertEqual(response.status_code, 401)

    def test_reservation_post_keyerror(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : access_token}
        data_input = {
            ""      : "20세",
            "time"  : "4:30 PM",
            "store" : "명동점",
            "date"  : "2020-07-12"
        }
        response = client.post('/reservation', json.dumps(data_input), **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'INVALID_KEY'})
        self.assertEqual(response.status_code, 400)

    def test_reservation_delete_success(self):
        client = Client()
        response = client.delete('/reservation?reservation_no=123', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_reservation_delete_no_value(self):
        client = Client()
        response = client.delete('/reservation?reservation_no=456', content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 401)

    def test_reservation_delete_keyerror(self):
        client = Client()
        response = client.delete('/reservation', content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'INVALID_KEY'})
        self.assertEqual(response.status_code, 400)

class ReservationCheckTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id   = 1,
            name = "male"
        )

        Account.objects.create(
            id       = 1,
            name     = "user",
            password = hashed_password.decode('utf-8'),
            gender   = Gender.objects.get(id = 1),
            phone    = "123456789",
            email    = "bmo@gmail.com"
        )

        Reservation.objects.create(
            reservation_number = "123",
            store              = "명동점",
            date               = "2020-07-20",
            time               = "5:30 PM",
            age                = "20~25세",
            account            = Account.objects.get(id = 1)
        )

    def tearDown(self):
        Gender.objects.all().delete()
        Account.objects.all().delete()
        Reservation.objects.all().delete()

    def test_reservation_check_get_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : access_token}
        response = client.get('/reservation/check', **header, content_type = 'application/json')
        result = {
            "reservation_list": [
                {
                    "reservation_no": "123",
                    "reservation_store": "명동점",
                    "reservation_date": "2020-07-20",
                    "reservation_time": "5:30 PM",
                    "name": "user",
                    "phone": "123456789"
                }
            ]
        }
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_reservation_check_get_fail(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : '1'}
        response = client.get('/reservation/check', **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'INVALID_TOKEN'})
        self.assertEqual(response.status_code, 400)

class ReservationUpdateTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id   = 1,
            name = "male"
        )

        Account.objects.create(
            id       = 1,
            name     = "user",
            password = hashed_password.decode('utf-8'),
            gender   = Gender.objects.get(id = 1),
            phone    = "123456789",
            email    = "bmo@gmail.com"
        )

        Reservation.objects.create(
            reservation_number = "123",
            store              = "명동점",
            date               = "2020-07-20",
            time               = "5:30 PM",
            age                = "20~25세",
            account            = Account.objects.get(id = 1)
        )

    def tearDown(self):
        Gender.objects.all().delete()
        Account.objects.all().delete()
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
                "name": "user",
                "phone": "123456789"
            }
        }
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_reservation_update_get_no_value(self):
        client = Client()
        response = client.get('/reservation/update?reservation_no=789', content_type = 'application/json')

        self.assertEqual(response.json(), {'message' : 'DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 401)

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

    def test_reservation_update_put_no_value(self):
        client = Client()
        response = client.get('/reservation/update?reservation_no=789', content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 401)
