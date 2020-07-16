import json

from django.test import (
    TestCase,
    Client
)
from .models    import Shop

class ShopTest(TestCase):
    def setUp(self):
        client = Client()
        Shop.objects.create(
            name        =       "라네즈 플래그십 스토어 명동점",
            address     =       "서울특별시 중구 명동8길",
            latitude    =       43.12534,
            longitude   =       23.1235
        )

    def tearDown(self):
        Shop.objects.all().delete()
    
    def test_shop_search_success(self):
        client          =       Client()
        response        =      client.get("/shop/?search='명동'", content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_shop_search_fail(self):
        client          =      Client()
        response        =      client.get('/shop/?shop="중구"', content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_shop_search_empty(self):
        client      =   Client()
        response    =   client.get('/shop/?search="인천"', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'shops': []})