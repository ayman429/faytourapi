
from rest_framework import serializers
from .models import *
class TouristPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristPlaces
        fields =['id','name']