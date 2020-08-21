from django.db import models

class Account(models.Model):
    name     = models.CharField(max_length = 50)
    email    = models.CharField(max_length = 100)
    password = models.CharField(max_length = 1000)
    phone    = models.CharField(max_length = 50)
    gender   = models.ForeignKey('Gender', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = "accounts"

class Gender(models.Model):
    name   = models.CharField(max_length = 20)

    class Meta:
        db_table = "genders"
