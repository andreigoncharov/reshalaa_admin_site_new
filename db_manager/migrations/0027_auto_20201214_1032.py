# Generated by Django 3.1.1 on 2020-12-14 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_manager', '0026_auto_20201210_1238'),
    ]

    operations = [

        migrations.AddField(
            model_name='pays',
            name='author',
            field=models.CharField(blank=True, max_length=45, verbose_name='ord_id'),
        ),
    ]
