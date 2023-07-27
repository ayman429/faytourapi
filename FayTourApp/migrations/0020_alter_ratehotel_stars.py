# Generated by Django 3.2 on 2023-06-26 17:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FayTourApp', '0019_alter_ratehotel_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratehotel',
            name='stars',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]