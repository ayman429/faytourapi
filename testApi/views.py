from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from . models import *
from .serializers import *

class viewTouristPlaces(viewsets.ModelViewSet):
    queryset = TouristPlaces.objects.all()
    serializer_class = TouristPlacesSerializer