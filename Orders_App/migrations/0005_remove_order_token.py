# Generated by Django 4.0.3 on 2022-03-13 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders_App', '0004_order_active_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='token',
        ),
    ]
