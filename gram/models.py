from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from imagekit.models import ProcessedImageField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField(max_length = 30, blank = True)
    website = models.CharField(max_length = 30, blank = True)
    phone_number = models.IntegerField(blank = True, null = True)
    location = models.CharField(max_length = 30, blank = True)
    birth_date = models.DateField(null = True, blank = True)
    followers = models.ManyToManyField('Profile', related_name = 'followers_profile', blank = True)
    following = models.ManyToManyField('Profile', related_name = 'following_profile', blank = True)
    profile_pic = models.ImageField(upload_to = 'profile_pic/', null =True, blank = True)

    @receiver(post_save,sender = User)
    def create_user_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects