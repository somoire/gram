from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm,ProfileForm,PostForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User
from .models import Profile,Post,Comment,Like
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from annoying.decorators import ajax_request

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
  # Only return posts from users that are being followed
  users_followed = request.user.profile.following.all()
  posts = Post.objects.filter(profile__in=users_followed).order_by('-posted_on')


  return render(request,'index.html',{"posts":posts})

@login_required
@transaction.atomic
def update_profile(request, username):
  user = User.objects.get(username = username)
  if request.method == 'POST':
    user_form = UserForm(request.POST, instance = request.user)
    profile_form = ProfileForm(request.POST, instance = request.user.profile,files =request.FILES)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, ('Your profile was successfully updated!'))
      return redirect(reverse('profile', kwargs={'username': request.user.username}))
    else:
      messages.error(request, ('Please correct the error below.'))
  else:
    user_form = UserForm(instance = request.user)
    profile_form = ProfileForm(instance = request.user.profile)
  return render(request, 'profiles/profile_form.html', {"user_form": user_form,"profile_form": profile_form})


@login_required
def profile(request, username):
  user = User.objects.get(username = username)
  if not user:
    return redirect('Home')
  profile = Profile.objects.get(user =user)


  title = f"{user.username}"
  return render(request, 'profiles/profile.html', {"title": title, "user":user, "profile":profile})

def followers(request, username):
  user = user = User.objects.get(username = username)
  user_profile = Profile.objects.get(user=user)
  profiles = user_profile.followers.all

  title = "Followers"

  return render(request, 'follow_list.html', {"title": title, "profiles":profiles})

def following(request, username):
  user = user = User.objects.get(username = username)
  user_profile = Profile.objects.get(user=user)
  profiles = user_profile.following.all()

  title = "Following"

  return render(request, 'follow_list.html', {"title": title, "profiles":profiles})


@login_required
def posts(request):
  if request.method == 'POST':
    form = PostForm(request.POST,files = request.FILES)
    if form.is_valid():
      post = Post(profile = request.user.profile, title = request.POST['title'], image = request.FILES['image'])
      post.save()
      return redirect('profile', kwargs={'username':request.user.username})
  else:
    form = PostForm()
  return render(request, 'post_picture.html', {"form": form})

def post(request, pk):
    post = Post.objects.get(pk=pk)
    try:
        like = Like.objects.get(post=post, user=request.user)
        liked = 1
    except:
        like = None
        liked = 0

    return render(request, 'post.html', {"post": post})


def explore(request):
  random_posts = Post.objects.all().order_by('?')[:40]

  
  return render(request, 'explore.html', {"posts":random_posts})

def likes(request, pk):
  post = Post.objects.get(pk=pk)
  profiles = Like.objects.filter(post=post)

  title = 'Likes'
  return render(request, 'follow_list.html', {"title": title, "profiles":profiles})


@ajax_request
@login_required
def add_like(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
@login_required
def add_comment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username
        profile_url = reverse('profile', kwargs={'username': request.user})

        commenter_info = {
            'username': username,
            'profile_url': profile_url,
            'comment_text': comment_text
        }


        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }

@ajax_request
@login_required
def follow_toggle(request):
    user_profile = Profile.objects.get(user=request.user)
    follow_profile_pk = request.POST.get('follow_profile_pk')
    follow_profile = Profile.objects.get(pk=follow_profile_pk)

    try:
        if user_profile != follow_profile:
            if request.POST.get('type') == 'follow':
                user_profile.following.add(follow_profile)
                follow_profile.followers.add(user_profile)
            elif request.POST.get('type') == 'unfollow':
                user_profile.following.remove(follow_profile)
                follow_profile.followers.remove(user_profile)
            user_profile.save()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_profile_pk': follow_profile_pk
    }