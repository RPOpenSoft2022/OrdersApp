# Generated by Django 3.1.14 on 2022-03-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders_App', '0012_remove_order_active_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]