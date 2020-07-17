from django.db import models

from product.models import Product
# from order.models   import (
#     Order,
#     OrderProduct
# )

class Account(models.Model):
    name           = models.CharField(max_length = 50)
    birthdate      = models.CharField(max_length = 50)
    gender         = models.ForeignKey("Gender", on_delete = models.SET_NULL,null = True)
    password       = models.CharField(max_length = 1000, null = True)
    phone_number   = models.CharField(max_length = 50, null = True)
    user_email     = models.CharField(max_length = 100)
    is_social_user = models.CharField(max_length = 100 )
    # order          = models.ManyToManyField("order.Order", through = "OrderProduct")
    
    class Meta:
        db_table = "accounts"

class Gender(models.Model):
    name   = models.CharField(max_length = 20)
    
    class Meta:
        db_table = "genders"
