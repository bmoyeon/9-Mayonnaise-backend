import json
import base64
import datetime
import pytz
from    django.test import (
                                TestCase,
                                Client
)
from    freezegun                           import freeze_time
from    decimal                             import Decimal
from    django.forms.models                 import model_to_dict
from    django.core.files.uploadedfile      import SimpleUploadedFile
from    io                                  import BytesIO
from    laneige.settings                    import S3, S3_URL, ACCESS_KEY
from    account.models                      import Account
from    account.utils                       import login_required
from    .models                             import Review, SkinType
from    product.models                      import (
                                                        Product,
                                                        Type,
                                                        Category,
                                                        Menu,
                                                        Tag,
                                                        Series,
                                                        ProductCategory,
                                                        ProductTag,
                                                        ProductSeries
)

class Review_list_test(TestCase):
    @freeze_time("2020-07-10T00:00:00.00")
    def setUp(self):
        client      =   Client()

        user        =   Account.objects.create(
            id      =   1,
            name    =   "kyleHan"
        )

        skinType    =   SkinType.objects.create(
            id          =   1,
            skin_type   =   "건성"
        )
        menu        =   Menu.objects.create(
            id      =   1,
            name    =   "옴므"
        )
        p_type      =   Type.objects.create(
            id      =   1,
            name    =   "피부진정"
        )
        category    =   Category.objects.create(
            id          =   1,
            menu        =   menu,
            type_name   =   p_type
        )

        product     =   Product.objects.create(
            id                  =   1,
            name_ko             =   "에센셜 스킨 토너",
            name_en             =   "Essentail skin toner",
            description         =   "건성 피부의 보습력을 상승시켜주는 프리미엄 토너",
            price               =   23000,
            volume              =   "100ml",
            ingredient          =   "스킨 토너",
            feature             =   "",
        )

        review      =   Review.objects.create(
            id              =       1,
            user            =       user,
            product         =       product,
            skin_type       =       skinType,
            rate            =       4.5,
            comment         =       "라네즈를 사고 피부 완전 좋아졌어요",
            review_image    =       "image_url",
        )

    def tearDown(self):
        Account.objects.all().delete()
        Product.objects.all().delete()
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Type.objects.all().delete()
        SkinType.objects.all().delete()
        Review.objects.all().delete()
        
    @freeze_time("2020-07-10")
    def test_review_lsit_success(self):
        client          =       Client()
        review_test     =       Review.objects.get(id=1)
        reviews         =       [
            {
                "user_id"       :   review_test.user.name,
                "rate"          :   '4.5',
                "create_at"     :   "2020-07-10T00:00:00Z",
                "comment"       :   review_test.comment,
                "image"         :   review_test.review_image,
                "skin_type"     :   review_test.skin_type.skin_type,
                "total_count"   :   1
            }
        ]
        
        response        =       client.get("/review/?product_id=1", content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"reviews":reviews})

    def test_review_lsit_KeyError(self):
        client          =   Client()
        review_test     =   Review.objects.get(id =1)

        reviews         =       [
            {
                "user_id"       :   review_test.user.name,
                "rate"          :   review_test.rate,
                "created_at"    :   review_test.created_at,
                "comment"       :   review_test.comment,
                "image"         :   review_test.review_image,
                "skin_type"     :   review_test.skin_type.skin_type,
            }
        ]

        response        =       client.get("/review/?product=1", content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_review_list_Fail(self):
        client          =       Client()
        response        =       client.get("/review/?product_id=2", content_type='application/json')

        self.assertEqual(response.status_code, 401)

class ReviewInsertViewTest(TestCase):
    def setUp(self):
        client      =   Client()

        user        =   Account.objects.create(
            id      =   1,
            name    =   "kyleHan"
        )

        skinType    =   SkinType.objects.create(
            id          =   1,
            skin_type   =   "건성"
        )
        menu        =   Menu.objects.create(
            id      =   1,
            name    =   "옴므"
        )
        p_type      =   Type.objects.create(
            id      =   1,
            name    =   "피부진정"
        )
        category    =   Category.objects.create(
            id          =   1,
            menu        =   menu,
            type_name   =   p_type
        )
        product     =   Product.objects.create(
            id                  =   1,
            name_ko             =   "에센셜 스킨 토너",
            name_en             =   "Essentail skin toner",
            description         =   "건성 피부의 보습력을 상승시켜주는 프리미엄 토너",
            price               =   23000,
            volume              =   "100ml",
            ingredient          =   "스킨 토너",
            feature             =   "",
        )

    def tearDown(self):
        Account.objects.all().delete()
        Product.objects.all().delete()
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Type.objects.all().delete()
        SkinType.objects.all().delete()
        Review.objects.all().delete()

    @login_required
    def test_review_insert_success(self):
        client          =       Client()
        header          =       {"HTTP_AUTORIZATION":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.y42DGv-P8a3Toi_utiZPR4iX_HyxwrtCjCulT5ewtnQ"}
        img             =       BytesIO(b'randomImage')
        img.name        =       'junsu.jpg'
        forms            =       {
            "review_image": img,
            "product_id" :1,
            "skin_type_id" : 1,
            "rate" : "4.5",
            "comment" : "이미지 업로드 할거임"
            
        }
        response        =       self.client.post('/review/', forms, **header, content_type="application/json")
        self.assertEqual(response.status_code, 200)
