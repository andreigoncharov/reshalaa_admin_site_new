# Generated by Django 3.1.1 on 2020-12-07 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_manager', '0022_auto_20201026_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonuses',
            fields=[
                ('tel_id', models.CharField(blank=True, max_length=45, primary_key=True, serialize=False, verbose_name='Заказчик')),
                ('count_b', models.IntegerField(verbose_name='Количество бонусов')),
            ],
        ),
    ]