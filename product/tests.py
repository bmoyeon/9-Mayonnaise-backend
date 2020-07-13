<<<<<<< HEAD
import json

from django.test import (
    TestCase, 
    Client
)

from .models import (
    Menu,
    Type,
    Category,
    Product,
    ProductCategory,
    Tag,
    ProductTag,
    Image
)

class ProductTest(TestCase):
    def setUp(self):
        client = Client()

        Menu.objects.create(
            id   = 1,
            name = "스킨케어"
        )

        Type.objects.create(
            id   = 1,
            name = "클렌징"
        )

        Category.objects.create(
            id        = 1,
            menu      = Menu.objects.get(id = 1),
            type_name = Type.objects.get(id = 1)
        )

        Product.objects.create(
            id          = 1,
            name_ko     = "에센셜 밸런싱 스킨 리파이너 라이트",
            name_en     = "ESSENTIAL BALANCING SKIN REFINER LIGHT",
            description = "번들거리는 피부의 유수분 밸런스를 맞춰주고 피부 바탕을 맑게 정돈해주는 산뜻한 스킨이에요.",
            price       = 29000,
            volume      = "200ml",
            ingredient  = "정제수, 프로판다이올, 1,2-헥산다이올",
            feature     = "html"
        )

        Product.objects.create(
            id          = 2,
            name_ko     = "에센셜 밸런싱 로션 리파이너 라이트",
            name_en     = "ESSENTIAL BALANCING SKIN REFINER LIGHT",
            description = "번들거리는 피부의 유수분 밸런스를 맞춰주고 피부 바탕을 맑게 정돈해주는 산뜻한 로션이에요.",
            price       = 29000,
            volume      = "200ml",
            ingredient  = "정제수, 프로판다이올, 1,2-헥산다이올",
            feature     = "html"
        )

        ProductCategory.objects.create(
            id       = 1,
            product  = Product.objects.get(id = 1),
            category = Category.objects.get(id = 1)
        )

        Tag.objects.create(
            id   = 1,
            name = "지성피부"
        )

        Tag.objects.create(
            id   = 2,
            name = "산뜻한스킨"
        )

        ProductTag.objects.create(
            id      = 1,
            product = Product.objects.get(id = 1),
            tag     = Tag.objects.get(id = 1),
        )

        ProductTag.objects.create(
            id      = 2,
            product = Product.objects.get(id = 1),
            tag     = Tag.objects.get(id = 2),
        )
        
        Image.objects.create(
            id          = 1,
            image_url   = "https://thumb.png",
            product     = Product.objects.get(id = 1),
            is_main_img = True
        )

        Image.objects.create(
            id          = 2,
            image_url   = "https://thumb-03.png",
            product     = Product.objects.get(id = 2),
            is_main_img = True
        )

    def tearDown(self):
        Menu.objects.all().delete()
        Type.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        Tag.objects.all().delete()
        ProductTag.objects.all().delete()
        Image.objects.all().delete()

    def test_productlist_get_success(self):
        client   = Client()
        response = client.get('/product?menu_id=1', content_type = 'application/json')
        result = {
            "product_list": [
                {
                    "product_id": 1,
                    "product_name_ko": "에센셜 밸런싱 스킨 리파이너 라이트",
                    "product_tag": [
                        "지성피부",
                        "산뜻한스킨"
                    ],
                    "product_image": "https://thumb.png"
                }
            ]
        }

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)
    
    def test_productlist_get_not_found(self):
        client   = Client()
        response = client.get('/product?menu_id=8', content_type = 'application/json')

        self.assertEqual(response.status_code, 404)

    def test_productlist_keyerror(self):
        client   = Client()
        response = client.get('/product?types_id=1', content_type = 'application/json')

        self.assertEqual(response.status_code, 400)

class ProductDetailTest(TestCase):

    def setUp(self):
        client = Client()

        Product.objects.create(
            id = 1,
            name_ko = "스킨",
            name_en = "SKIN",
            description = "스킨이에요.",
            price = 29000.00,
            volume = "200ml",
            ingredient = "정제수",
            feature = "html"
        )
        
        Tag.objects.create(
            id = 1,
            name = "지성피부"
        )

        Tag.objects.create(
            id = 2,
            name = "산뜻한스킨"
        )

        ProductTag.objects.create(
            id = 1,
            product = Product.objects.get(id=1),
            tag = Tag.objects.get(id=1),
        )

        ProductTag.objects.create(
            id = 2,
            product = Product.objects.get(id=1),
            tag = Tag.objects.get(id=2),
        )
        
        Image.objects.create(
            id = 1,
            image_url = "https://thumb.png",
            product = Product.objects.get(id=1),
            is_main_img = 1
        )

    def tearDown(self):
        Product.objects.all().delete()
        Tag.objects.all().delete()
        ProductTag.objects.all().delete()
        Image.objects.all().delete()

    def test_productdetail_get_success(self):
        client = Client()
        response = client.get('/product/1', content_type = 'application/json')
        result = {
            "item": {

                "product_id": 1,
                "product_name_ko": "스킨",
                "product_name_en": "SKIN",
                "product_tag": [
                    "지성피부",
                    "산뜻한스킨"
                ],
                "product_description": "스킨이에요.",
                "product_price": "29000.00",
                "product_volume": "200ml",
                "product_images": [
                    "https://thumb.png"
                ],
                "product_ingredient": "정제수",
                "product_feature": "html",
            }  
        }

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)
    
    def test_productdetail_get_not_found(self):
        client = Client()
        response = client.get('/product/2', content_type = 'application/json')
        
        self.assertEqual(response.status_code, 404)
    
    def test_productdetail_keyerror(self):
        client = Client()
        response = client.get('/product', content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
=======
from django.test import TestCase

# Create your tests here.
>>>>>>> e91a8e6... shop model views, test done & review testing
