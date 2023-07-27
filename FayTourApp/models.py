from datetime import datetime
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db.models import Avg
from django.core.validators import FileExtensionValidator
import os

# ------- model
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from User.models import CustomUser
# Create your models here.

class TouristPlaces(models.Model):
    name = models.CharField(max_length=500,unique=True)
    nameAR = models.CharField(max_length=500,default='')
    type = models.CharField(max_length=500)
    description = models.TextField(default='')
    descriptionAR = models.TextField(default='')
    coordinatesX = models.FloatField()
    coordinatesY = models.FloatField()
    address = models.CharField(max_length=100)
    originalImage = models.ImageField(upload_to='image')
    # video = models.FileField(upload_to='video',validators=[FileExtensionValidator(allowed_extensions=["mp4"])])
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    class Meta:
       unique_together = ("coordinatesX", "coordinatesY")

    def no_of_ratings(self):
        ratings = RateTouristPlaces.objects.filter(touristPlaces=self)
        return len(ratings)

    def avg_ratings(self):
        avg = RateTouristPlaces.objects.filter(touristPlaces=self).aggregate(Avg('stars'))['stars__avg']
        if avg is not None: return avg
        return 0.0

    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=500,unique=True)
    nameAR = models.CharField(max_length=500,default='')
    description = models.TextField(default='')
    descriptionAR = models.TextField(default='')
    coordinatesX = models.FloatField(default=0.0)
    coordinatesY = models.FloatField(default=0.0)
    originalImage = models.ImageField(upload_to='image')
    address = models.CharField(max_length=500)
    City = models.CharField(max_length=500)
    TotalBeds = models.IntegerField(default=0)
    Phone = models.CharField(max_length=500,unique=True)
    web = models.CharField(max_length=500,default='')
    email = models.EmailField(default='')
    Single = models.IntegerField(default=0)
    Double = models.IntegerField(default=0)
    Triple = models.IntegerField(default=0)
    Sweet  = models.IntegerField(default=0)
    chalet = models.IntegerField(default=0)
    villa  = models.IntegerField(default=0)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    def no_of_ratings(self):
        ratings = RateHotel.objects.filter(hotel=self)
        return len(ratings)

    def avg_ratings(self):
        avg = RateHotel.objects.filter(hotel=self).aggregate(Avg('stars'))['stars__avg']
        if avg is not None: return avg
        return 0.0

    def totalRooms(self):
        sum = self.Single+self.Double+self.Triple+self.Sweet+self.chalet+self.villa
        if sum !=0: return sum
        return 0

class HotelsImages(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="image",blank=True,unique=True)

class TourismImages(models.Model):
    touristPlaces = models.ForeignKey(TouristPlaces,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="image",blank=True,unique=True)

class RateTouristPlaces(models.Model):
    touristPlaces = models.ForeignKey(TouristPlaces,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])


    class Meta:
        unique_together = (('user', 'touristPlaces'),)
        index_together = (('user', 'touristPlaces'),)

class RateHotel(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'hotel'),)
        index_together = (('user', 'hotel'),)


# ----------------------------------------------------------
class Post(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    body=models.TextField(default="")
    index = models.CharField(max_length=500,default="")
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True) # default=datetime.now() auto_now_add=True
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True) # auto_now=True

    class Meta:
        ordering = ['-created_at']

def get_unique_filename(instance, filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename, ext = os.path.splitext(filename)
    unique_filename = f"{filename}_{timestamp}{ext}"
    folder = "image/posts"
    return os.path.join(folder, unique_filename)

class PostImages(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to=get_unique_filename,blank=True,unique=True,default="")

# ----------------------------------------------------------
class LikePost(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    like = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(1)])

    class Meta:
        unique_together = (('user', 'post'),)
        index_together = (('user', 'post'),)
# ----------------------------------------------------------
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    comment =  models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True) # default=datetime.now() auto_now_add=True
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True) # auto_now=True
    current_time = timezone.now()
    # class Meta:
    #     ordering = ['-created_at']

# ----------------------------------------------------------
class FavoriteHotel(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    fav = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(1)])

    class Meta:
        unique_together = (('user', 'hotel'),)
        index_together = (('user', 'hotel'),)

# ----------------------------------------------------------
class FavoriteTouristPlaces(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    touristPlaces = models.ForeignKey(TouristPlaces,on_delete=models.CASCADE)
    fav = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    class Meta:
        unique_together = (('user', 'touristPlaces'),)
        index_together = (('user', 'touristPlaces'),)

# ----------------------------------------------------------
class HotelReservation(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    adulls = models.PositiveSmallIntegerField()
    kids = models.PositiveSmallIntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True) # default=datetime.now() auto_now_add=True
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True) # auto_now=True
    class Meta:
        unique_together = (('user', 'hotel'),)
        index_together = (('user', 'hotel'),)


# ---------------------- AI MODEL --------------------
# def get_recommendations(name):
#         # Load data from API
#         place_response = 'https://faytourapp.pythonanywhere.com/api/TourismPlace/'
#         place_headers = {
#             'Authorization': 'Token 37bb23be1fa2003096eb8498920cb0a8be81f2f8'
#         }

#         place_response_obj = requests.get(
#             place_response, headers=place_headers)
#         place_data = pd.DataFrame(place_response_obj.json())
#         place_data.drop_duplicates(subset='name', keep='first', inplace=True)
#         place_data.dropna(subset=['description', 'type'], inplace=True)
#         place_data.reset_index(inplace=True, drop=True)
#         tfidf_vectorizer = TfidfVectorizer(stop_words='english')
#         place_tfidf = tfidf_vectorizer.fit_transform(place_data['description'])
#         user_tfidf = tfidf_vectorizer.transform([name])
#         similarity_scores = cosine_similarity(
#             user_tfidf, place_tfidf).flatten()
#         place_data['similarity_score'] = similarity_scores
#         place_data = place_data[place_data['similarity_score'] > 0]
#         place_data.sort_values(by='similarity_score',
#                               ascending=False, inplace=True)
#         recommendations = place_data

#         return recommendations








