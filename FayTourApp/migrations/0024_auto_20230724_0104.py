# Generated by Django 3.2 on 2023-07-23 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FayTourApp', '0023_auto_20230722_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='descriptionAR',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='hotel',
            name='nameAR',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='touristplaces',
            name='descriptionAR',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='touristplaces',
            name='nameAR',
            field=models.CharField(default='', max_length=500),
        ),
    ]
