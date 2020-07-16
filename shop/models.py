from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=500)
    contact = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=8, decimal_places=3)
    longitude = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        db_table = 'shops'
