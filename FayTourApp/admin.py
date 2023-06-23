from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(TouristPlaces)
admin.site.register(Hotel)
admin.site.register(RateTouristPlaces)
admin.site.register(RateHotel)