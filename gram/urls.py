from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from .import views


urlpatterns =[
  url(r'^$', views.index, name='Home'),
  url(r'^profile/(?P<username>[-_\w.]+)/$', views.profile, name='profile'),
  url(r'^profile/(?P<username>[-_\w.]+)/edit/$', views.update_profile, name='edit'),
  url(r'^profile/(?P<username>[-_\w.]+)/followers/$', views.followers, name='followers'),
  url(r'^profile/(?P<username>[-_\w.]+)/following/$', views.following, name='following'),
  url(r'^post/$', views.posts, name='post_picture'),
  url(r'^post/(?P<pk>\d+)/$', views.post, name='post'),
  url(r'^explore/$', views.explore, name='explore'),
  url(r'^like/$', views.add_like, name='like'),
  url(r'^comment/$', views.add_comment, name='comment'),
  url(r'^follow_toggle/$', views.follow_toggle, name='follow_toggle'),
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )