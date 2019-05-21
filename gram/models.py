from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='./media/')


# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE)
  bio = models.TextField(max_length = 30, blank = True)
  website = models.CharField(max_length=30, blank =True)
  phone_number = models.IntegerField(blank =True, null = True)
  location = models.CharField(max_length = 30, blank =True)
  birth_date = models.DateField(null =True, blank = True)
  followers = models.ManyToManyField('Profile', related_name = 'followers_profile', blank =True)
  following = models.ManyToManyField('Profile', related_name='following_profile', blank =True)
  profile_pic = models.ImageField(storage=fs, null =True, blank = True)


  @receiver(post_save,sender = User)
  def create_user_profile(sender,instance,created, **kwargs):
    if created:
      Profile.objects.create(user=instance)

  @receiver(post_save,sender = User)
  def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()

  def get_number_of_followers(self):
    if self.followers.count():
      return self.followers.count()
    else:
      return 0

  def get_number_of_following(self):
    if self.following.count():
      return self.following.count()
    else:
      return 0
  def __str__(self):
    return self.user.username


class Post(models.Model):
  profile = models.ForeignKey(Profile, null = True, blank = True, on_delete = models.CASCADE)
  title = models.CharField(max_length = 100)
  image = models.ImageField(storage=fs)
  posted_on = models.DateTimeField(auto_now_add=True)

  def get_number_of_likes(self):
    return self.like_set.count()

  def get_number_of_comments(self):
    return self.comment_set.count()


class Comment(models.Model):
  post = models.ForeignKey('Post', on_delete = models.CASCADE)
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  comment = models.CharField(max_length = 100)
  post_on = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.comment


class Like(models.Model):
  post = models.ForeignKey('Post', on_delete = models.CASCADE)
  user = models.ForeignKey(User, on_delete = models.CASCADE)

  class Meta:
    unique_together = ("post", "user")

  def __str__(self):
    return 'Like:' + self.user.username + ' ' + self.post.title