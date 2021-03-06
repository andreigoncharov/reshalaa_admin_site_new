# Generated by Django 3.1.1 on 2020-10-01 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_manager', '0010_auto_20201001_0920'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceO',
            fields=[
                ('ord_id', models.IntegerField(editable=False, primary_key=True, serialize=False, verbose_name='Номер заказа')),
                ('tel_id', models.CharField(blank=True, max_length=45, null=True, verbose_name='Заказчик')),
                ('type', models.CharField(blank=True, max_length=80, null=True, verbose_name='Тип')),
                ('prof', models.CharField(blank=True, max_length=80, null=True, verbose_name='Профиль')),
                ('predm', models.CharField(blank=True, max_length=80, null=True, verbose_name='Предмет')),
                ('info', models.CharField(blank=True, max_length=3000, null=True, verbose_name='Информация')),
                ('oforml', models.CharField(blank=True, max_length=60, null=True, verbose_name='Оформление')),
                ('date', models.CharField(blank=True, max_length=45, null=True, verbose_name='Дата сдачи')),
                ('time', models.CharField(blank=True, max_length=45, null=True, verbose_name='Время сдачи')),
                ('end_contr', models.CharField(blank=True, max_length=45, null=True, verbose_name='Окончание контроля')),
                ('price', models.CharField(blank=True, max_length=45, null=True, verbose_name='Цена')),
                ('links', models.URLField(blank=True, max_length=5000, null=True, verbose_name='Ссылки на документы')),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Username')),
            ],
        ),
    ]
