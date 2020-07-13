from django.db          import models
from account.models     import Account
from product.models     import Product

# class Order(models.Model):
#     user        =       models.ForeignKey("Account", on_delete=models.SET_NULL, null =True)
#     product     =       models.ForeignKey("Product", on_delete=models.SET_NULL, null =True)
#     amount      =       models.IntegerField(default=1)
#     created_at  =       models.DateTimeField(auto_now_add=True)

#     class Mete:
#         db_table    =   "orders"
