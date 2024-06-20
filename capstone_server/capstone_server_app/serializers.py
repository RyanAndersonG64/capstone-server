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

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = Group
    fields = '__all__'

class FriendInviteSerializer(serializers.ModelSerializer):
  class Meta:
    model = FriendInvite
    fields = '__all__'

class GroupInviteSerializer(serializers.ModelSerializer):
  class Meta:
    model = GroupInvite
    fields = '__all__'

class GroupJoinRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = GroupJoinRequest
    fields = '__all__'

class GroupMessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = GroupMessage
    fields = '__all__'