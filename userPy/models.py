from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import ugettext_lazy

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(('email address'), unique=True)
    image = models.ImageField(upload_to='usersImages/',default="")
    is_manager = models.BooleanField(default=False)
    managerId = models.PositiveSmallIntegerField(default=0)
    placeType = models.CharField(max_length=200,default="")
    model1Input = models.TextField(default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    spouse_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.email
