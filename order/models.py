from django.db import models

from account.models import Account
from product.models import Product,Image


class OrderProduct(models.Model):
    order       = models.ForeignKey("Order", on_delete = models.SET_NULL, null = True)
    product     = models.ForeignKey("product.Product", on_delete = models.SET_NULL, null = True)
    price       = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity    = models.IntegerField(null=True)

    class Meta:
        db_table = "order_products"

class Order(models.Model):
    account          = models.ForeignKey("account.Account", on_delete = models.SET_NULL, null = True)
    status           = models.ForeignKey("OrderStatus", on_delete = models.SET_NULL, null = True)
    order_date       = models.DateTimeField(auto_now_add = True, null= True)
    address          = models.TextField(null=True)
    product          = models.ManyToManyField("product.Product", through = "OrderProduct")
    total_price      = models.DecimalField(max_digits = 10, decimal_places = 2, null=True)
    
    class Meta:
        db_table = "orders"

class OrderStatus(models.Model):
    name  = models.CharField(max_length = 50)
    
    class Meta:
        db_table = "order_status"
