from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, viewsets

from .models import *
from .serializers import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
  user = request.user
  profile = user.profile
  serializer = ProfileSerializer(profile, many=False)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
  profiles = Profile.objects.all()
  all_profiles_serializer = ProfileSerializer(profiles, many=True)
  return Response(all_profiles_serializer.data)

@api_view(['POST'])
@permission_classes([])
def create_user(request):
    user = User.objects.create(
        username = request.data['username'],
    )
    user.set_password(request.data['password'])
    user.save()
    profile = Profile.objects.create(
        user=user,
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )
    profile.save()
    profile_serialized = ProfileSerializer(profile)
    return Response(profile_serialized.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_credit(request):
   user_id = request.data['user_id']
   user = Profile.objects.get(id = user_id)

   request.data['user'] = user.user.id
   request.data['first_name'] = user.first_name
   request.data['last_name'] = user.last_name
   request.data['coaster_count'] = user.coaster_count
   request.data['favorites'] = user.favorites

   user.coasters_ridden.append(request.data['coaster_id'])

   serialized_user = ProfileSerializer(user, data = request.data)
   if serialized_user.is_valid():
      serialized_user.save()
      return Response(serialized_user.data)
   else:
      return Response(serialized_user.errors)
   
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_credit(request):
   user_id = request.data['user_id']
   user = Profile.objects.get(id = user_id)

   request.data['user'] = user.user.id
   request.data['first_name'] = user.first_name
   request.data['last_name'] = user.last_name
   request.data['coaster_count'] = user.coaster_count
   request.data['favorites'] = user.favorites

   user.coasters_ridden.remove(request.data['coaster_id'])

   serialized_user = ProfileSerializer(user, data = request.data)
   if serialized_user.is_valid():
      serialized_user.save()
      return Response(serialized_user.data)
   else:
      return Response(serialized_user.errors)
   
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def set_favorite(request):
    user_id = request.data['id']
    user = Profile.objects.get(id = user_id)

    request.data['user'] = user.user.id
    request.data['first_name'] = user.first_name
    request.data['last_name'] = user.last_name
    request.data['coaster_count'] = user.coaster_count

    rank = request.data['rank']
    coaster = request.data['coaster']
    print(rank)
    user.favorites.insert(rank-1, f"{coaster}")
    user.favorites.pop(rank)

    serialized_user = ProfileSerializer(user, data = request.data)
    if serialized_user.is_valid():
        serialized_user.save()
        return Response(serialized_user.data)
    else:
        return Response(serialized_user.errors)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_post(request):
  poster_id = request.data['posted_by']
  poster = Profile.objects.get(id=poster_id)
  poster_name = poster.first_name
  post = ForumPost.objects.create (
    title = request.data['title'],
    posted_by = poster, #update to find user with requested id
    poster_name = poster_name,
    text_content = request.data['text_content'],
  )
  post.likes.set([])
  serialized_post = ForumPostSerializer(post, data=request.data)
  if serialized_post.is_valid():
    serialized_post.save()
    return Response(serialized_post.data)
  return Response(serialized_post.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
@parser_classes([MultiPartParser, FormParser])
def get_posts(request):
  posts = ForumPost.objects.all()
  posts_serialized = ForumPostSerializer(posts, many=True)
  return Response(posts_serialized.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_post(request):
    print(f'request = {request.data}')
    post_pk = request.data['post_pk']
    print(f'post pk ={post_pk}')
    post = ForumPost.objects.get(pk=post_pk)
    request.data['posted_by'] = post.posted_by.id
    new_text = request.data['text_content']
    post.text_content = new_text
    request.data['poster_name'] = post.posted_by.first_name
    print(post)
    serialized_post = ForumPostSerializer(post, data = request.data)
    print(serialized_post)
    if serialized_post.is_valid():
      serialized_post.save()
      return Response(serialized_post.data)
    else:
      return Response(serialized_post.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request):
    post_pk = request.data['postId']
    print(f'post pk ={post_pk}')
    post = ForumPost.objects.get(pk=post_pk)
    post.delete()
    return Response('DELORTED')

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def like_post(request):
   user = request.data['current_user']
   profile = Profile.objects.get(pk = user)
   post_pk = request.data['post_id']
   post = ForumPost.objects.get(pk = post_pk)
   request.data['posted_by'] = post.posted_by.id
   request.data['text_content'] = post.text_content
   if post.likes.filter(pk = post_pk).exists:
      post.likes.add(user)
      post.liked_by.add(user)
      print(post.likes)
   serialized_post = ForumPostSerializer(post, data = request.data)
   print(serialized_post)
   if serialized_post.is_valid():
      serialized_post.save()
      return Response(serialized_post.data)
   else:
      return Response(serialized_post.errors)