# Generated by Django 3.0.7 on 2020-07-14 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(null=True),
        ),
    ]
