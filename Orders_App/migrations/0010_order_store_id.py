# Generated by Django 4.0.3 on 2022-03-16 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders_App', '0009_order_delivery_otp_order_delivery_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='store_id',
            field=models.BigIntegerField(default=12),
            preserve_default=False,
        ),
    ]
