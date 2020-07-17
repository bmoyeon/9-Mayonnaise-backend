from django.db import models

class Reservation(models.Model):
    reservation_number = models.CharField(max_length = 50)
    store              = models.CharField(max_length = 100)
    date               = models.CharField(max_length = 50)
    created_at         = models.DateTimeField(auto_now_add = True, null = True)
    time               = models.CharField(max_length = 20)
    age                = models.CharField(max_length = 50)
    account            = models.ForeignKey("account.Account", on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = "reservations"