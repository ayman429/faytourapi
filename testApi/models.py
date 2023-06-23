from django.db import models

# Create your models here.


class TouristPlaces(models.Model):
    name = models.CharField(max_length=500,unique=True)