# Generated by Django 3.1.1 on 2020-10-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_manager', '0009_auto_20200930_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_price',
            name='customer_pr',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Цена для заказчика'),
        ),
        migrations.AlterField(
            model_name='customer_price',
            name='price',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Цена автора'),
        ),
    ]
