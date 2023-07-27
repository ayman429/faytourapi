from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('TourismPlace',viewTouristPlaces)
router.register('Hotel',viewHotel)
router.register('RateTourismPlace',viewRateTouristPlaces)
router.register('RateHotel',viewRateHotel)
router.register('Post',viewPost)
router.register('comment',viewComment)
router.register('LikePost',viewLikePost)
router.register('HotelReservation',viewHotelReservation)
router.register('FavoriteHotel',viewFavoriteHotel)

urlpatterns = [
    path('', include(router.urls)),
]
