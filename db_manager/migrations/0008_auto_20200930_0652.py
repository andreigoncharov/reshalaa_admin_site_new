# Generated by Django 3.1.1 on 2020-09-30 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_manager', '0007_auto_20200930_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ord_auth_price',
            name='ord_id',
            field=models.IntegerField(default=1, editable=False, primary_key=True, serialize=False, verbose_name='Номер заказа'),
        ),
    ]
