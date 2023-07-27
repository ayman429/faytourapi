from django.shortcuts import render
from rest_framework import viewsets
from . models import *
from .serializers import *
from User.models import CustomUser

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django.db.models import Avg
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status

import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class viewTouristPlaces(viewsets.ModelViewSet):
    search_fields = ['name','description','nameAR','descriptionAR','address','type']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)

    ordering_fields = ['name', 'address','type']

    queryset = TouristPlaces.objects.all()
    serializer_class = TouristPlacesSerializer

    @action(detail=False, methods=['Get'])
    def model1(self, request):
        data = request.data
        userInput = data['input']
        # Process the input data using your AI model
        # result = get_recommendations(userInput)  # Call your AI model's prediction function

        ############################################
        obj=TouristPlaces.objects.all()
        data_places=[]
        for place in obj:
            data_places.append({"id":place.id,"name":place.name,"description":place.description,"type":place.type})

        place_data = pd.DataFrame(data_places)
        place_data.drop_duplicates(subset='name', keep='first', inplace=True)
        place_data.dropna(subset=['description', 'type'], inplace=True)
        place_data.reset_index(inplace=True, drop=True)
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        place_tfidf = tfidf_vectorizer.fit_transform(place_data['description'])
        user_tfidf = tfidf_vectorizer.transform([userInput])
        similarity_scores = cosine_similarity(
            user_tfidf, place_tfidf).flatten()
        place_data['similarity_score'] = similarity_scores
        place_data = place_data[place_data['similarity_score'] > 0]
        place_data.sort_values(by='similarity_score',
                              ascending=False, inplace=True)
        recommendations = place_data
        result = recommendations
        # ############################################

        ids = result['id'].tolist()
        names = result['name'].tolist()
        similarity_scores = result['similarity_score'].tolist()
        listData = []
        for i in range(len(ids)):
            touristPlace = TouristPlaces.objects.get(id =ids[i])
            serializer = TouristPlacesSerializer(touristPlace,context={'request': request})
            listData.append(serializer.data)
        return Response(listData)


    @action(detail=False, methods=['Get'])
    def getFav(self, request):
        placeId = request.data['placeId']
        place = TouristPlaces.objects.get(id=placeId)
        userId = request.data['userId']
        try:
          favorite = FavoriteTouristPlaces.objects.get(user=userId,touristPlaces=place)
          return Response({"favorite":str(favorite.fav)})
        except:
            return Response({"massage":"no favorite"})

    @action(detail=False, methods=['Get'])
    def getFavorite(self,request):
        userId = request.data['userId']
        favPlaces = FavoriteTouristPlaces.objects.filter(user=userId,fav=1)
        listPlaces=[]
        for i in range(len(favPlaces)):
            touristPlace=TouristPlaces.objects.get(id=favPlaces[i].touristPlaces.id)
            serializer = TouristPlacesSerializer(touristPlace,context={'request': request})
            listPlaces.append(serializer.data)
        return Response(listPlaces)

    @action(detail=True, methods=['post'])
    def fav(self, request, pk=None):
        if 'fav' in request.data:
            place = TouristPlaces.objects.get(id=pk)
            userId = request.data['user']
            user = CustomUser.objects.get(id=userId)
            addfav= request.data['fav']
            if int(addfav) ==0 or int(addfav) ==1:
                # update:
                try:
                    favorite = FavoriteTouristPlaces.objects.get(user=userId,touristPlaces=place)
                    favorite.fav = addfav
                    favorite.save()
                    serializer = FavoriteTouristPlacesSerializer(favorite,many = False)
                    json = {
                        'message': 'TouristPlaces Favorite Updated',
                        'result': serializer.data
                    }
                    return Response(json)
                # create:
                except:
                    favorite = FavoriteTouristPlaces.objects.create(user=user,touristPlaces=place,fav=addfav)
                    serializer = FavoriteTouristPlacesSerializer(favorite,many = False)
                    json = {
                        'message': 'TouristPlaces Favorite Created',
                        'result': serializer.data
                    }
                    return Response(json)
            return Response({"fav": ["fav must be 0 or 1."]},status.HTTP_400_BAD_REQUEST)
        return Response({"fav": ["This field is required."]},status.HTTP_400_BAD_REQUEST)


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
            if int(stars) >=1 and int(stars) <=5:
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
            return Response({"stars": ["stars must be between 1 and 5."]},status.HTTP_400_BAD_REQUEST)
        return Response({"stars": ["This field is required."]},status.HTTP_400_BAD_REQUEST)

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
            if average_stars is not None and average_stars >= max_average-1:
                json.append(obj.id)

        for i in range(len(json)):
            TouristPlaces_by_rateNamber = TouristPlaces.objects.get(id = json[i])
            serializer = TouristPlacesSerializer(TouristPlaces_by_rateNamber,context={'request': request})
            json2.append(serializer.data)
        json2 = sorted(json2, key=lambda x: float(x['avg_ratings']), reverse=True)
        return Response(json2)

class viewHotel(viewsets.ModelViewSet):

    search_fields = ['name','description','nameAR','descriptionAR','address','City','Phone','TotalBeds']
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

    @action(detail=False, methods=['Get'])
    def getFavorite(self,request):
        userId = request.data['userId']
        favPlaces = FavoriteHotel.objects.filter(user=userId,fav=1)
        listhotels=[]
        for i in range(len(favPlaces)):
            hotel=Hotel.objects.get(id=favPlaces[i].hotel.id)
            serializer = HotelSerializer(hotel,context={'request': request})
            listhotels.append(serializer.data)
        return Response(listhotels)

    @action(detail=True, methods=['post'])
    def fav(self, request, pk=None):
        if 'fav' in request.data:
            hotel = Hotel.objects.get(id=pk)
            userId = request.data['user']
            user = CustomUser.objects.get(id=userId)
            addfav= request.data['fav']
            if int(addfav) ==0 or int(addfav) ==1:
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
            return Response({"fav": ["fav must be 0 or 1."]},status.HTTP_400_BAD_REQUEST)
        return Response({"fav": ["This field is required."]},status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['Get'])
    def getRate_Hotel(self, request):
        hotelId = request.data['hotelId']
        hotel = Hotel.objects.get(id=hotelId)
        userId = request.data['userId']
        print(hotelId)
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
            if int(stars) >=1 and int(stars) <=5:
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
            return Response({"stars": ["stars must be between 1 and 5."]},status.HTTP_400_BAD_REQUEST)
        return Response({"stars": ["This field is required."]},status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['Get'])
    def searchRateNamber(self, request):
        json = []
        json2 = []
        max_average = 0
        for obj in Hotel.objects.all():
            average_stars =RateHotel.objects.filter(hotel=obj).aggregate(Avg('stars'))['stars__avg']
            if average_stars is not None and average_stars > max_average:
                max_average = average_stars

        for obj in Hotel.objects.all():
            average_stars =RateHotel.objects.filter(hotel=obj).aggregate(Avg('stars'))['stars__avg']
            if average_stars is not None and average_stars >= max_average-1:
                json.append(obj.id)

        for i in range(len(json)):
            hotels_by_rateNamber = Hotel.objects.get(id = json[i])
            serializer = HotelSerializer(hotels_by_rateNamber,context={'request': request})
            json2.append(serializer.data)
        json2 = sorted(json2, key=lambda x: float(x['avg_ratings']), reverse=True)
        return Response(json2)

    # def get_serializer_class(self):
    #     return HotelSerializer

class viewRateTouristPlaces(viewsets.ModelViewSet):
    queryset = RateTouristPlaces.objects.all()
    serializer_class = RateTouristPlacesSerializer

class viewRateHotel(viewsets.ModelViewSet):
    queryset = RateHotel.objects.all()
    serializer_class = RateHotelSerializer
# ---------------------------------------
class viewFavoriteTouristPlaces(viewsets.ModelViewSet):
    queryset = FavoriteTouristPlaces.objects.all()
    serializer_class = FavoriteTouristPlacesSerializer

class viewFavoriteHotel(viewsets.ModelViewSet):
    queryset = FavoriteHotel.objects.all()
    serializer_class = FavoriteHotelSerializer
# ---------------------------------------
class viewPost(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    ordering_fields = ['created_at']

    @action(detail=False, methods=['Get'])
    def getLike(self, request):
        postId = request.data['postId']
        post = Post.objects.get(id=postId)
        userId = request.data['userId']
        try:
          like = LikePost.objects.get(user=userId,post=post)
          return Response({"like":str(like.like)})
        except:
            return Response({"like":"0"})

    @action(detail=True, methods=['post'])
    def addLike(self, request, pk=None):
        if 'like' in request.data:
            post = Post.objects.get(id=pk)
            userId = request.data['user']
            user = CustomUser.objects.get(id=userId)
            addLike= request.data['like']
            if int(addLike) ==0 or int(addLike) ==1:
                # update:
                try:
                    like = LikePost.objects.get(user=userId,post=post)
                    like.like = addLike
                    like.save()
                    serializer = LikePostSerializer(like,many = False)
                    json = {
                        'message': 'Post Like Updated',
                        'result': serializer.data
                    }
                    return Response(json)
                # create:
                except:
                    like = LikePost.objects.create(user=user,post=post,like=addLike)
                    serializer = LikePostSerializer(like,many = False)
                    json = {
                        'message': 'Post Like Created',
                        'result': serializer.data
                    }
                    return Response(json)
            return Response({"like": ["like must be 0 or 1."]},status.HTTP_400_BAD_REQUEST)
        return Response({"postId": ["This field is required."]},status.HTTP_400_BAD_REQUEST)
# ---------------------------------------
class viewLikePost(viewsets.ModelViewSet):
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer
# ---------------------------------------
class viewComment(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=False, methods=['Get'])
    def getCommentByPostId(self, request):
        if 'postId' in request.data:
            postId = request.data['postId']
            post = Post.objects.get(id=postId)

            try:
                comments = Comment.objects.filter(post=post)
                list=[]
                for i in range(len(comments)):
                    list.append({"id":comments[i].id,"comment":comments[i].comment,"created_at":comments[i].created_at,
                        "updated_at":comments[i].updated_at,"current_time":comments[i].current_time,
                        "created_by": {
                            "id": comments[i].user.id,
                            "userName": comments[i].user.username,
                            "email": comments[i].user.email,
                            "image": comments[i].user.image.url if comments[i].user.image else ""
                            }
                        })
                return Response(list)
            except:
                return Response({"massage":"no Comment"})
        return Response({"postId": ["This field is required."]},status.HTTP_400_BAD_REQUEST)


# ---------------------------
class viewHotelReservation(viewsets.ModelViewSet):
    queryset = HotelReservation.objects.all()
    serializer_class = HotelReservationSerializer

    @action(detail=False, methods=['Get'])
    def getHotelReservation(self, request):
        if 'hotelId' in request.data:
            hotelId = request.data['hotelId']
            hotel = Hotel.objects.get(id=hotelId)

            try:
                reservation = HotelReservation.objects.filter(hotel=hotel)
                list=[]

                for i in range(len(reservation)):
                    list.append({
                        "id":reservation[i].id,
                        "phone_number":reservation[i].phone_number,
                        "adulls":reservation[i].adulls,"kids":reservation[i].kids,
                        "check_in":reservation[i].check_in,"check_out":reservation[i].check_out,
                        "created_at":reservation[i].created_at,"updated_at":reservation[i].updated_at,
                        "created_by": {
                            "id": reservation[i].user.id,
                            "userName": reservation[i].user.username,
                            "email": reservation[i].user.email,
                            "image": reservation[i].user.image.url if reservation[i].user.image else ""
                            }
                        })
                return Response(list)
            except:
                return Response({"massage":"no Reservation"})
        return Response({"hotelId": ["This field is required."]},status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['Get'])
    def getHotelReservationByUser(self, request):
        if 'user' in request.data:
            userId = request.data['user']
            base_url= 'https://faytourimages.s3.amazonaws.com/'
            try:
                reservation = HotelReservation.objects.filter(user=userId)
                list=[]

                for i in range(len(reservation)):
                    hotel = Hotel.objects.get(id=reservation[i].hotel.id)
                    print(base_url+"/"+str(hotel.originalImage))
                    list.append({
                        "id":reservation[i].id,
                        "hotel":reservation[i].hotel.id,
                        "hotelImage":base_url+str(hotel.originalImage),
                        "hotelName":hotel.name,
                        "hotelNameAR":hotel.nameAR,
                        "phone_number":reservation[i].phone_number,
                        "adulls":reservation[i].adulls,"kids":reservation[i].kids,
                        "check_in":reservation[i].check_in,"check_out":reservation[i].check_out,
                        "created_at":reservation[i].created_at,"updated_at":reservation[i].updated_at,
                        })
                return Response(list)
            except:
                return Response({"massage":"no Reservation"})
        return Response({"user": ["This field is required."]},status.HTTP_400_BAD_REQUEST)


# ---------------------------
# class Model1(APIView):

#     def post(self, request):
#         data = request.data
#         userInput = data['input']
#         # Process the input data using your AI model
#         result = get_recommendations(userInput)  # Call your AI model's prediction function
#         # json_data = result.to_json(orient='records')
#         ids = result['id'].tolist()
#         names = result['name'].tolist()
#         similarity_scores = result['similarity_score'].tolist()
#         # Convert DataFrame to JSON
#         # json_data = result.to_json(orient='records')
#         # return JsonResponse({'prediction': json_data})
#         # listData = []
#         # for i in range(len(ids)):
#         #     TouristPlace = TouristPlaces.objects.get(id = ids[i])
#         #     serializer = TouristPlacesSerializer(TouristPlaces)
#         #     listData.append(serializer.data)
#         return JsonResponse({'ids': ids,'names': names, "similarity_scores":similarity_scores})





