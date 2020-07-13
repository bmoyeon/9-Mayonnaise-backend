import os
import django
import csv
import sys
from shop.models import shop


def insert():
    with open('shop.csv') as csv_master:
        csv_read = csv.reader(csv_master)
        next(csv_read, None)
        for row in csv_read:
            if not row[2].startswith("0"):
                phone = "0" + row[2]
            phone = row[2]
            shop.objects.create(
                name=row[0],
                address=row[1],
                contact=phone,
                latitude = row[3],
                longitude = row[4]
            )
