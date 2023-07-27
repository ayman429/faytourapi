from User.serializers import UserSerializer
from rest_framework import serializers
from .models import *


class TourismImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourismImages
        fields = ['image']

class HotelImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelsImages
        fields = ['image']

class TouristPlacesSerializer(serializers.ModelSerializer):
    images = TourismImagesSerializer(many=True,read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length=1000000,allow_empty_file=False,use_url=False),
        write_only=True
    )

    rate_one_by_one = serializers.SerializerMethodField('rate_one_by_one_func')
    created_by = serializers.SerializerMethodField('touristPlaces_created_by')

    rate_value = serializers.SerializerMethodField('get_rate_value')
    fav_value = serializers.SerializerMethodField('get_fav_value')

    def get_rate_value(self, touristPlaces):
        request = self.context.get('request')
        try:
            rate = RateTouristPlaces.objects.get(touristPlaces=touristPlaces, user=request.user)
            return rate.stars
        except RateTouristPlaces.DoesNotExist:
            return 0

    def get_fav_value(self, touristPlaces):
        request = self.context.get('request')
        try:
            fav = FavoriteTouristPlaces.objects.get(touristPlaces=touristPlaces, user=request.user)
            return fav.fav
        except FavoriteTouristPlaces.DoesNotExist:
            return 0


    class Meta:
        model = TouristPlaces
        fields = ['id','name','nameAR','type','address','description','descriptionAR','coordinatesX','coordinatesY','originalImage',
                  'uploaded_images','images','no_of_ratings','avg_ratings','rate_one_by_one','user','created_by','rate_value','fav_value']# 'video',

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        touristPlaces = TouristPlaces.objects.create(**validated_data)

        for image in uploaded_images:
            new_image = TourismImages.objects.create(touristPlaces=touristPlaces, image=image)
        return touristPlaces

    def rate_one_by_one_func(request,self):
        ratings = RateTouristPlaces.objects.filter(touristPlaces=self)
        length = len(ratings)
        star1 = RateTouristPlaces.objects.filter(touristPlaces=self,stars=1).count()
        star2 = RateTouristPlaces.objects.filter(touristPlaces=self,stars=2).count()
        star3 = RateTouristPlaces.objects.filter(touristPlaces=self,stars=3).count()
        star4 = RateTouristPlaces.objects.filter(touristPlaces=self,stars=4).count()
        star5 = RateTouristPlaces.objects.filter(touristPlaces=self,stars=5).count()
        if length !=0:
            list_of_rate = {"1":int((star1/length)*100),"2":int((star2/length)*100),"3":int((star3/length)*100),
                            "4":int((star4/length)*100),"5":int((star5/length)*100)}

        else: list_of_rate = {"1":0,"2":0,"3":0,"4":0,"5":0}

        return list_of_rate

    def touristPlaces_created_by(request,self):
        json = {
            "id":self.user.id,
            "userName":self.user.username,
            "email":self.user.email
            }
        print(json)
        return json


class HotelSerializer(serializers.ModelSerializer):
    images = HotelImagesSerializer(many=True,read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length=1000000,allow_empty_file=False,use_url=False),
        write_only=True
    )

    rate_one_by_one = serializers.SerializerMethodField('rate_one_by_one_func')
    created_by = serializers.SerializerMethodField('hotel_created_by')
    # x= UserSerializer(read_only=True, many=True)

    rate_value = serializers.SerializerMethodField('get_rate_value')
    fav_value = serializers.SerializerMethodField('get_fav_value')

    def get_rate_value(self, hotel):
        request = self.context.get('request')
        try:
            rate = RateHotel.objects.get(hotel=hotel, user=request.user)
            return rate.stars
        except RateHotel.DoesNotExist:
            return 0

    def get_fav_value(self, hotel):
        request = self.context.get('request')
        try:
            fav = FavoriteHotel.objects.get(hotel=hotel, user=request.user)
            return fav.fav
        except FavoriteHotel.DoesNotExist:
            return 0

    class Meta:
        model = Hotel
        fields = ['id','name','nameAR','description','descriptionAR','coordinatesX','coordinatesY','address','City','Phone','web','email',
                  'Single','Double','Triple','Sweet','chalet','villa','totalRooms','TotalBeds',
                  'no_of_ratings','avg_ratings','rate_one_by_one','images','originalImage','uploaded_images','user','created_by','rate_value','fav_value'
                ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        hotel = Hotel.objects.create(**validated_data)

        for image in uploaded_images:
            newproduct_image = HotelsImages.objects.create(hotel=hotel, image=image).image
            # print("newimage: ",newproduct_image)
        return hotel

    def rate_one_by_one_func(request,self):
        ratings = RateHotel.objects.filter(hotel=self)
        length = len(ratings)
        star1 = RateHotel.objects.filter(hotel=self,stars=1).count()
        star2 = RateHotel.objects.filter(hotel=self,stars=2).count()
        star3 = RateHotel.objects.filter(hotel=self,stars=3).count()
        star4 = RateHotel.objects.filter(hotel=self,stars=4).count()
        star5 = RateHotel.objects.filter(hotel=self,stars=5).count()
        if length !=0:
            list_of_rate = {"1":int((star1/length)*100),"2":int((star2/length)*100),"3":int((star3/length)*100),
                            "4":int((star4/length)*100),"5":int((star5/length)*100)}

        else: list_of_rate = {"1":0,"2":0,"3":0,"4":0,"5":0}
        return list_of_rate

    def hotel_created_by(request,self):
        json = {
            "id":self.user.id,
            "userName":self.user.username,
            "email":self.user.email
            }
        return json

class RateTouristPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateTouristPlaces
        fields = '__all__'

class RateHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateHotel
        fields = '__all__'



# --------------------------------------------------------
class FavoriteTouristPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteTouristPlaces
        fields = ['id','user','touristPlaces','fav']
# --------------------------------------------------------
class FavoriteHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteHotel
        fields = ['id','user','hotel','fav']

# --------------------------------------------------------
class PostImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ['image']

class PostSerializer(serializers.ModelSerializer):
    images = PostImagesSerializer(many=True,read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length=1000000,allow_empty_file=False), # use_url=False
        write_only=True,
        required=False
    )
    comment_numbers = serializers.SerializerMethodField('number_of_comments_func')
    like_numbers = serializers.SerializerMethodField('number_of_likes_func')
    created_by = serializers.SerializerMethodField('post_created_by')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    like_value = serializers.SerializerMethodField()

    def get_like_value(self, post):
        request = self.context.get('request')
        try:
            like = LikePost.objects.get(post=post, user=request.user)
            return like.like
        except LikePost.DoesNotExist:
            return 0

    class Meta:
        model = Post
        fields = ['id','user','body','index','uploaded_images','images','created_by','created_at','updated_at','comment_numbers','like_numbers','like_value']


    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images",[])
        post = Post.objects.create(**validated_data)

        for image in uploaded_images:
            new_image = PostImages.objects.create(post=post, image=image)
        return post

    def update(self, instance, validated_data):
        instance.body = validated_data.get("body", instance.body)
        instance.index = validated_data.get("index", instance.index)
        instance.save()
        uploaded_images = validated_data.pop("uploaded_images", [])
        images_queryset = instance.images.all()
        indexS=instance.index.replace(",", "")
        if instance.index !="-1":
            for i in range(len(indexS)):
                images_queryset[int(indexS[i])].delete()
        # Create new images if there are more uploaded_images than current_images
        for image in uploaded_images:
            PostImages.objects.create(post=instance, image=image)
        return instance

    def number_of_comments_func(request,self):
        Commentnumbers = Comment.objects.filter(post=self).count()
        return str(Commentnumbers)

    def number_of_likes_func(request,self):
        Likenumbers = LikePost.objects.filter(post=self,like=1).count()
        return str(Likenumbers)

    def post_created_by(request,self):
        json = {
            "id":self.user.id,
            "userName":self.user.username,
            "email":self.user.email,
            "image":self.user.image.url if self.user.image else ""
            }
        print(json)
        return json

# --------------------------------------------------------
class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ['id','user','post','like']
# --------------------------------------------------------
class CommentSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField('comment_created_by')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Comment
        fields = ['id','user','post','comment','created_by','created_at','updated_at','current_time']

    def comment_created_by(request,self):
        json = {
            "id":self.user.id,
            "userName":self.user.username,
            "email":self.user.email,
            "image":self.user.image.url if self.user.image else ""
            }
        print(json)
        return json

# --------------------------------------------------------
class HotelReservationSerializer(serializers.ModelSerializer):
    # created_by = serializers.SerializerMethodField('comment_created_by')
    # created_at = serializers.DateField(format='%Y-%m-%d', required=False)
    # updated_at = serializers.DateField(format='%Y-%m-%d', required=False)

    class Meta:
        model = HotelReservation
        fields = ['id','user','hotel','phone_number','adulls','kids','check_in','check_out','created_at','updated_at']




