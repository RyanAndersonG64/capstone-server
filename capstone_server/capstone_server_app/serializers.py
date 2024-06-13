from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
  likes = serializers.IntegerField(source = 'likes.count', read_only = True)
  class Meta:
    model = Image
    fields = '__all__'

class ForumPostSerializer(serializers.ModelSerializer):
  likes = serializers.IntegerField(source = 'likes.count', read_only = True)
  class Meta:
    model = ForumPost
    fields = '__all__'