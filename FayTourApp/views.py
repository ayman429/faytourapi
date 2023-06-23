# from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from . models import *
from .serializers import *
from User.models import CustomUser

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django.db.models import Avg,Max

# -----------
from rest_framework.views import APIView
# from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import get_recommendations

# from rest_framework.decorators import api_view

# class viewTouristPlacesTopRated(viewsets.ModelViewSet):
#     queryset = TouristPlaces.objects.filter(touristPlaces=obj).aggregate(Avg('stars'))['stars__avg']
#     serializer_class = TouristPlacesSerializer

class viewTouristPlaces(viewsets.ModelViewSet):
    search_fields = ['name','description','address','type']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)

    ordering_fields = ['name', 'address','type']

    queryset = TouristPlaces.objects.all()
    serializer_class = TouristPlacesSerializer
     
    @action(detail=False, methods=['Get'])
    def getFav(self, request):
        hotelId = request.data['hotelId']
        hotel = Hotel.objects.get(id=hotelId)
        userId = request.data['userId']
        try:
          favorite = FavoriteTouristPlaces.objects.get(user=userId,hotel=hotel)
          return Response({"favorite":str(favorite.fav)})
        except:
            return Response({"massage":"no favorite"})

    @action(detail=True, methods=['post'])
    def fav(self, request, pk=None):
        if 'fav' in request.data:
            hotel = Hotel.objects.get(id=pk)
            userId = request.data['user']
            user = CustomUser.objects.get(id=userId)
            addfav= request.data['fav']
            # update:
            try:
                favorite = FavoriteTouristPlaces.objects.get(user=userId,hotel=hotel)
                favorite.fav = addfav
                favorite.save()
                serializer = FavoriteTouristPlacesSerializer(favorite,many = False)
                json = {
                    'message': 'Hotel Favorite Updated',
                    'result': serializer.data
                }
                return Response(json)
            # create:
            except:    
                favorite = FavoriteTouristPlaces.objects.create(user=user,hotel=hotel,fav=addfav)
                serializer = FavoriteTouristPlacesSerializer(favorite,many = False)
                json = {
                    'message': 'Hotel Favorite Created',
                    'result': serializer.data
                }
                return Response(json)
        return Response("json")
    

    @action(detail=False, methods=['Get'])
    def getRate_TourismPlace(self, request):
        placeId = request.data['placeId']
        touristPlaces = TouristPlaces.objects.get(id=placeId)
        userId = request.data['userId']
        try:
          rating = RateTouristPlaces.objects.get(user=userId,touristPlaces=touristPlaces)
          return Response({"star":str(rating.stars)})
        except:
            return Response({"massage":"no rate"})
        
        

    @action(detail=True, methods=['post'])
    def rate_TourismPlace(self, request, pk=None):
        if 'stars' in request.data:
            touristPlaces = TouristPlaces.objects.get(id=pk)
            stars = request.data['stars']
            username = request.data['username']
            user = CustomUser.objects.get(id=username)
            # update:
            try:
                rating = RateTouristPlaces.objects.get(user=username,touristPlaces=touristPlaces)
                rating.stars = stars
                rating.save()
                serializer = RateTouristPlacesSerializer(rating,many = False)
                json = {
                    'message': 'Tourism Place Rate Updated',
                    'result': serializer.data
                }
                return Response(json)
            # create:
            except:    
                rating = RateTouristPlaces.objects.create(user=user,touristPlaces=touristPlaces,stars=stars)
                serializer = RateTouristPlacesSerializer(rating,many = False)
                json = {
                    'message': 'Tourism Place Rate Created',
                    'result': serializer.data
                }
                return Response(json)
        return Response("json")
    
    @action(detail=False, methods=['Get'])
    def searchRateNamber(self, request):
        json = []
        json2 = []
        max_average = 0
        for obj in TouristPlaces.objects.all(): 
            average_stars =RateTouristPlaces.objects.filter(touristPlaces=obj).aggregate(Avg('stars'))['stars__avg']
            if average_stars is not None and average_stars > max_average:
                max_average = average_stars
        
        for obj in TouristPlaces.objects.all(): 
            average_stars =RateTouristPlaces.objects.filter(touristPlaces=obj).aggregate(Avg('stars'))['stars__avg']
            if average_stars is not None and average_stars == max_average:
                json.append(obj.id)
 
        for i in range(len(json)):
            TouristPlaces_by_rateNamber = TouristPlaces.objects.get(id = json[i])
            serializer = TouristPlacesSerializer(TouristPlaces_by_rateNamber)
            json2.append(serializer.data)
        json2 = sorted(json2, key=lambda x: x['average_stars'], reverse=True)
        return Response(json2) # , status=status.HTTP_200_OK

class viewHotel(viewsets.ModelViewSet):

    search_fields = ['name','description','address','City','Phone','TotalBeds']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)

    ordering_fields = ['name', 'address']

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    @action(detail=False, methods=['Get'])
    def getFav(self, request):
        hotelId = request.data['hotelId']
        hotel = Hotel.objects.get(id=hotelId)
        userId = request.data['userId']
        try:
          favorite = FavoriteHotel.objects.get(user=userId,hotel=hotel)
          return Response({"favorite":str(favorite.fav)})
        except:
            return Response({"massage":"no favorite"})

    @action(detail=True, methods=['post'])
    def fav(self, request, pk=None):
        if 'fav' in request.data:
            hotel = Hotel.objects.get(id=pk)
            userId = request.data['user']
            user = CustomUser.objects.get(id=userId)
            addfav= request.data['fav']
            # update:
            try:
                favorite = FavoriteHotel.objects.get(user=userId,hotel=hotel)
                favorite.fav = addfav
                favorite.save()
                serializer = FavoriteHotelSerializer(favorite,many = False)
                json = {
                    'message': 'Hotel Favorite Updated',
                    'result': serializer.data
                }
                return Response(json)
            # create:
            except:    
                favorite = FavoriteHotel.objects.create(user=user,hotel=hotel,fav=addfav)
                serializer = FavoriteHotelSerializer(favorite,many = False)
                json = {
                    'message': 'Hotel Favorite Created',
                    'result': serializer.data
                }
                return Response(json)
        return Response("json")
    

    @action(detail=False, methods=['Get'])
    def getRate_Hotel(self, request):
        hotelId = request.data['hotelId']
        hotel = Hotel.objects.get(id=hotelId)
        userId = request.data['userId']
        try:
          rating = RateHotel.objects.get(user=userId,hotel=hotel)
          return Response({"star":str(rating.stars)})
        except:
            return Response({"massage":"no rate"})

    @action(detail=True, methods=['post'])
    def rate_Hotel(self, request, pk=None):
        if 'stars' in request.data:
            hotel = Hotel.objects.get(id=pk)
            stars = request.data['stars']
            username = request.data['username']
            user = CustomUser.objects.get(id=username)
            # update:
            try:
                rating = RateHotel.objects.get(user=username,hotel=hotel)
                rating.stars = stars
                rating.save()
                serializer = RateHotelSerializer(rating,many = False)
                json = {
                    'message': 'Hotel Rate Updated',
                    'result': serializer.data
                }
                return Response(json)
            # create:
            except:    
                rating = RateHotel.objects.create(user=user,hotel=hotel,stars=stars)
                serializer = RateHotelSerializer(rating,many = False)
                json = {
                    'message': 'Hotel Rate Created',
                    'result': serializer.data
                }
                return Response(json)
        return Response("json")
 
    @action(detail=False, methods=['Get'])
    def searchRateNamber(self, request):
        json = []
        json2 = []
        max_average = 0
        for obj in Hotel.objects.all(): 
            average_stars =RateHotel.objects.filter(touristPlaces=obj).aggregate(Avg('stars'))['stars__avg']
            if average_stars is not None and average_stars > max_average:
                max_average = average_stars
        
        for obj in Hotel.objects.all(): 
            average_stars =RateHotel.objects.filter(touristPlaces=obj).aggregate(Avg('stars'))['stars__avg']
            if average_stars is not None and average_stars == max_average:
                json.append(obj.id)
 
        for i in range(len(json)):
            TouristPlaces_by_rateNamber = Hotel.objects.get(id = json[i])
            serializer = HotelSerializer(TouristPlaces_by_rateNamber)
            json2.append(serializer.data)
        return Response(json2)
        # json = []
        # json2 = []
        # RateNamber = request.data['RateNamber']
        # for obj in Hotel.objects.all(): 
        #     if RateHotel.objects.filter(hotel=obj).aggregate(Avg('stars'))['stars__avg'] == float(RateNamber):
        #         json.append(obj.id)
 
        # for i in range(len(json)):
        #     hotels_by_rateNamber = Hotel.objects.get(id = json[i])
        #     serializer = HotelSerializer(hotels_by_rateNamber)
        #     json2.append(serializer.data)
        # return Response(json2) # , status=status.HTTP_200_OK
   
    # def get_serializer_class(self):
    #     return HotelSerializer
    
class viewRateTouristPlaces(viewsets.ModelViewSet):
    queryset = RateTouristPlaces.objects.all()
    serializer_class = RateTouristPlacesSerializer

class viewRateHotel(viewsets.ModelViewSet):
    queryset = RateHotel.objects.all()
    serializer_class = RateHotelSerializer

# ---------------------------------------    
class viewPost(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    ordering_fields = ['created_at']
    

class Model1(APIView):

    def post(self, request):
        data = request.data
        userInput = data['input']
        # Process the input data using your AI model
        result = get_recommendations(userInput)  # Call your AI model's prediction function
        # json_data = result.to_json(orient='records')
        ids = result['id'].tolist()
        names = result['name'].tolist()
        similarity_scores = result['similarity_score'].tolist()
        # Convert DataFrame to JSON
        # json_data = result.to_json(orient='records')
        # return JsonResponse({'prediction': json_data})
        # listData = []
        # for i in range(len(ids)):
        #     TouristPlace = TouristPlaces.objects.get(id = ids[i])
        #     serializer = TouristPlacesSerializer(TouristPlaces)
        #     listData.append(serializer.data)
        return JsonResponse({'ids': ids,'names': names, "similarity_scores":similarity_scores})