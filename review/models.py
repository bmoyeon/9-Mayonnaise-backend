from account.models import Account
from product.models import Product
from django.db import models

class Review(models.Model):
    product         =       models.ForeignKey(Product, on_delete=models.CASCADE)
    user            =       models.ForeignKey(Account, on_delete=models.CASCADE)
    skin_type       =       models.ForeignKey('SkinType', on_delete=models.CASCADE)
    rate            =       models.DecimalField(max_digits=2, decimal_places=1)
    created_at      =       models.DateTimeField(auto_now_add=True)
    comment         =       models.CharField(max_length = 500)
    review_image    =       models.URLField(max_length = 2000, blank = True, null=True)
    
    class Meta:
        db_table    =       'reviews'

class SkinType(models.Model):
    skin_type       =       models.CharField(max_length =45)

    class Meta:
        db_table    =       'skintype'