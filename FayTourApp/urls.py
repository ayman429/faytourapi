from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('TourismPlace',viewTouristPlaces)
router.register('Hotel',viewHotel)
router.register('RateTourismPlace',viewTouristPlaces)
router.register('RateHotel',viewRateHotel)
router.register('Post',viewPost)
# router.register('model1',Model1)
# path('model1/', Model1.as_view(), name = 'Model1'),
# router.register('Favorite',viewFavorite)
urlpatterns = [
    path('', include(router.urls)),
    path('model1/', Model1.as_view())
]
