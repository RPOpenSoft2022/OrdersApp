# Generated by Django 4.0.3 on 2022-03-13 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders_App', '0003_alter_item_order_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='active_status',
            field=models.BooleanField(default=True),
        ),
    ]
