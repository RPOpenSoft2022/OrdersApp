# Generated by Django 4.0.3 on 2022-03-25 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders_App', '0015_item_item_price_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='store_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]