# -*- coding: utf-8 -*-
import json
import boto3
import uuid
import urllib.parse
from PIL import Image
from io import BytesIO
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from datetime import datetime
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.shortcuts import get_object_or_404
from laneige.settings import S3, S3_URL
from account.models import Account
from product.models import Product
from account.utils import login_required
from .models import (
    Review,
    SkinType
)
from django.http import (
    HttpResponse,
    JsonResponse
)


class ReivewView(View):
    # aws s3 connection
    s3_client = boto3.client(
        's3',
        aws_access_key_id=S3['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=S3['AWS_SECRET_ACCESS_KEY']
    )

    # totlalist & filter 출력
    def get(self, request):
        try:
            page = request.GET.get("page", 1)
            if 'product_id' not in request.GET.keys():
                raise KeyError

            filters = {
                'product_id':   request.GET.get('product_id'),
                'skin_type_id':   request.GET.get('skin_type_id')
            }

            if 'order_by' in request.GET.keys():
                order = {request.GET.get('order_by')}
            order = {}

            if 'skin_type_id' not in request.GET.keys():
                del filters['skin_type_id']

            if not Product.objects.filter(id=request.GET.get('product_id')).exists():
                raise Product.DoesNotExist

            reiview_list = Review.objects.filter(**filters).order_by(**order)
            paginator = Paginator(reiview_list, 9)
            total_count = paginator.count
            review_li = paginator.get_page(page)
            reviews = [
                {
                    "user_id":   review.user.name,
                    "rate":   review.rate,
                    "create_at":   review.created_at,
                    "comment":   review.comment,
                    "image":   review.review_image,
                    "skin_type":   review.skin_type.skin_type,
                    "total_count":   total_count
                }
                for review in review_li
            ]

            return JsonResponse({'reviews': reviews}, status=200)

        except Product.DoesNotExist:
            return HttpResponse(status=404)

        except KeyError:
            return HttpResponse(status=400)

    @login_required
    def delete(self, request):
        data = json.loads(request.body)
        try:
            if not Account.objects.get(id=data['user_id']) or Review.objects.get(user_id=data['user_id']):
                raise KeyError

            user = Account.objects.get(id=data['user_id'])
            Review.objects.get(user_id=user.id).delete()

            return HttpResponse(status=200)

        except KeyError:
            HttpResponse(status=400)

    @login_required
    def post(self, request, format=None):
        user = request.user_id
        product = Product.objects.get(id=request.POST.get('product_id'))
        skin = SkinType.objects.get(skin_type=request.POST.get('skin_type_id'))
        image_time = (str(datetime.now())).replace(" ", "")
        image_url = ""

        if request.FILES:
            image = request.FILES['review_image']
            image_name = request.POST.get("filename")
            image_type = (image.content_type).split("/")[1]
            self.s3_client.upload_fileobj(
                image,
                "mayonez",
                image_time+"."+image_type,
                ExtraArgs={
                    "ContentType": image.content_type
                }
            )

            image_url = S3_URL+image_time+"."+image_type
            image_url = image_url.replace(" ", "/")

        new_review = Review.objects.create(
            user=user,
            product=product,
            skin_type=skin,
            rate=request.POST.get('rate'),
            comment=request.POST.get('comment'),
            review_image=image_url
        )
        new_review = model_to_dict(
            new_review, fields=['user', 'product', 'skin_type', 'rate', 'review_image'])

        return JsonResponse({'review': new_review}, status=200)
