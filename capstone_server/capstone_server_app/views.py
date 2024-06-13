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