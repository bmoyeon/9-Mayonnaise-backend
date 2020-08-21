import json

from django.test import (
    TestCase,
    Client
)

from .models import (
    Menu,
    Category,
    Pair,
    Product,
    ProductPair,
    Tag,
    ProductTag,
    Image,
    Series,
    ProductSeries
)

class ProductListTest(TestCase):
    def setUp(self):
        Menu.objects.create(
            id   = 1,
            name = "스킨케어"
        )

        Category.objects.create(
            id   = 1,
            name = "클렌징"
        )

        Pair.objects.create(
            id       = 1,
            menu     = Menu.objects.get(id = 1),
            category = Category.objects.get(id = 1)
        )

        Product.objects.create(
            id          = 1,
            name_ko     = "스킨",
            name_en     = "SKIN",
            description = "스킨이에요.",
            price       = 29000,
            volume      = "200ml",
            ingredient  = "정제수",
            feature     = "html"
        )

        Product.objects.create(
            id          = 2,
            name_ko     = "로션",
            name_en     = "LOTION",
            description = "로션이에요.",
            price       = 29000,
            volume      = "200ml",
            ingredient  = "정제수",
            feature     = "html"
        )

        ProductPair.objects.create(
            id      = 1,
            product = Product.objects.get(id = 1),
            pair    = Pair.objects.get(id = 1)
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
        Category.objects.all().delete()
        Pair.objects.all().delete()
        Product.objects.all().delete()
        ProductPair.objects.all().delete()
        Tag.objects.all().delete()
        ProductTag.objects.all().delete()
        Image.objects.all().delete()

    def test_product_list_get_success(self):
        client   = Client()
        response = client.get('/product/list?menu_id=1', content_type = 'application/json')
        result = {
            "product_list": [
                {
                    "product_id": 1,
                    "product_name_ko": "스킨",
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

    def test_product_list_get_menu_not_found(self):
        client   = Client()
        response = client.get('/product/list?menu_id=10', content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 404)

    def test_product_list_get_category_not_found(self):
        client   = Client()
        response = client.get('/product/list?category_id=10', content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 404)

class ProductDetailTest(TestCase):
    def setUp(self):
        Product.objects.create(
            id          = 1,
            name_ko     = "스킨",
            name_en     = "SKIN",
            description = "스킨이에요.",
            price       = 29000.00,
            volume      = "200ml",
            ingredient  = "정제수",
            feature     = "html"
        )

        Product.objects.create(
            id          = 2,
            name_ko     = "로션",
            name_en     = "LOTION",
            description = "로션입니다.",
            price       = 29000.00,
            volume      = "200ml",
            ingredient  = "정제수",
            feature     = "html"
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

        ProductTag.objects.create(
            id      = 3,
            product = Product.objects.get(id = 2),
            tag     = Tag.objects.get(id = 1),
        )

        Image.objects.create(
            id          = 1,
            image_url   = "https://thumb.png",
            product     = Product.objects.get(id = 1),
            is_main_img = 1
        )

        Image.objects.create(
            id          = 2,
            image_url   = "https://thumb.png",
            product     = Product.objects.get(id = 2),
            is_main_img = 1
        )

        Series.objects.create(
            id   = 1,
            name = "블루에너지"
        )

        ProductSeries.objects.create(
            id      = 1,
            step    = "step1",
            product = Product.objects.get(id = 2),
            series  = Series.objects.get(id = 1)
        )

    def tearDown(self):
        Product.objects.all().delete()
        Tag.objects.all().delete()
        ProductTag.objects.all().delete()
        Image.objects.all().delete()
        Series.objects.all().delete()
        ProductSeries.objects.all().delete()

    def test_product_detail_get_success(self):
        client = Client()
        response = client.get('/product/1', content_type = 'application/json')
        result = {
            "product_info": {
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

    def test_product_detail_series_get_success(self):
        client = Client()
        response = client.get('/product/2', content_type = 'application/json')
        result = {
            "product_info": {
                "product_id": 2,
                "product_name_ko": "로션",
                "product_name_en": "LOTION",
                "product_tag": [
                    "지성피부"
                ],
                "product_description": "로션입니다.",
                "product_price": "29000.00",
                "product_volume": "200ml",
                "product_images": [
                    "https://thumb.png"
                ],
                "product_ingredient": "정제수",
                "product_feature": "html",
                "product_series": [{
                    "product_id": 2,
                    "product_name_ko": "로션",
                    "product_image": "https://thumb.png",
                    "step": "step1"
                }]
            }
        }
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_get_not_found(self):
        client = Client()
        response = client.get('/product/10', content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 404)
