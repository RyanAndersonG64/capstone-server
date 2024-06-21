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


# -- Managing user's ride history --


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
    user.favorites.insert(rank-1, f"{coaster}")
    user.favorites.pop(rank)

    serialized_user = ProfileSerializer(user, data = request.data)
    if serialized_user.is_valid():
        serialized_user.save()
        return Response(serialized_user.data)
    else:
        return Response(serialized_user.errors)
    

# -- stuff for user profiles --


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_profile_view(request):
   user = Profile.objects.get(pk = request.data['user'])

   request.data['coaster_count'] = user.coaster_count
   request.data['first_name'] = user.first_name
   request.data['last_name'] = user.last_name

   user.profile_view_state = request.data['new_state']

   serialized_user = ProfileSerializer(user, data = request.data)
   if serialized_user.is_valid():
      serialized_user.save()
      return Response(serialized_user.data)
   else:
      return Response(serialized_user.errors)


# -- CRUD for forum posts --

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_post(request):
  poster_id = request.data['posted_by']
  poster = Profile.objects.get(id=poster_id)
  poster_name = poster.first_name
  request.data['poster_name'] = poster_name
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
    post_pk = request.data['post_pk']
    post = ForumPost.objects.get(pk=post_pk)
    request.data['posted_by'] = post.posted_by.id

    new_text = request.data['text_content']
    post.text_content = new_text
    request.data['poster_name'] = post.posted_by.first_name
    request.data['liked_by'] = [like.pk for like in post.liked_by.all()]
    serialized_post = ForumPostSerializer(post, data = request.data)
    if serialized_post.is_valid():
      serialized_post.save()
      return Response(serialized_post.data)
    else:
      return Response(serialized_post.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request):
    post_pk = request.data['postId']
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


   if post.likes.filter(pk=profile.pk).exists():
        # If user already liked the post, remove the like
        post.likes.remove(profile)
        post.liked_by.remove(profile)
   else:
        # Add like if the user hasn't liked the post yet
        post.likes.add(profile)
        post.liked_by.add(profile)
   print([like.pk for like in post.liked_by.all()])
    # Prepare the data for serialization
   request_data = {
        'title': post.title,
        'posted_by': post.posted_by.id,
        'poster_name': post.poster_name,
        'posted_at': post.posted_at,
        'text_content': post.text_content,
        'likes': post.likes,
        'liked_by': [like.pk for like in post.liked_by.all()],
    }

   serialized_post = ForumPostSerializer(post, data = request_data)
   if serialized_post.is_valid():
      serialized_post.save()
      return Response(serialized_post.data)
   else:
      return Response(serialized_post.errors)
   

# -- CRUD for images --
   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_image(request):
  poster = Profile.objects.get(id = request.data['posted_by'])
  request.data['poster_name'] = poster.first_name

  image_serialized = ImageSerializer(data=request.data)
  if image_serialized.is_valid():
    image_serialized.save()
    return Response(image_serialized.data, status.HTTP_201_CREATED)
  return Response(image_serialized.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_images(request):
  images = Image.objects.all()
  images_serialized = ImageSerializer(images, many=True)
  return Response(images_serialized.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_image(request):
  image_pk = request.data['imageId']
  image = Image.objects.get(pk=image_pk)

  image.delete()
  return Response('DELORTED')

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def like_image(request):
   user = request.data['current_user']
   image_pk = request.data['image']
   image = Image.objects.get(pk = image_pk)

   image.likes.add(user)
   image.liked_by.add(user)

   serialized_image = ImageSerializer(image, data = request.data)
   if serialized_image.is_valid():
      serialized_image.save()
      return Response(serialized_image.data)
   else:
      return Response(serialized_image.errors)
   

# -- CRUD for Comments --


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request):
  poster_id = request.data['posted_by']
  poster = Profile.objects.get(id=poster_id)
  poster_name = poster.first_name
  post_id = request.data['post_id']
  post = ForumPost.objects.get(id = post_id)
  request.data['post'] = post.pk
  request.data['poster_name'] = poster_name
  
  comment = Comment.objects.create (
    post = post,
    posted_by = poster, #update to find user with requested id
    poster_name = poster_name,
    text_content = request.data['text_content'],
  )

  serialized_comment = CommentSerializer(comment, data=request.data)
  if serialized_comment.is_valid():
    serialized_comment.save()
    return Response(serialized_comment.data)
  return Response(serialized_comment.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
@parser_classes([MultiPartParser, FormParser])
def get_comments(request):
  comments = Comment.objects.all()
  comments_serialized = CommentSerializer(comments, many=True)
  return Response(comments_serialized.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_comment(request):
    comment_pk = request.data['comment_pk']
    comment = Comment.objects.get(pk=comment_pk)
    request.data['posted_by'] = comment.posted_by.id

    new_text = request.data['text_content']
    comment.text_content = new_text
    request.data['poster_name'] = comment.posted_by.first_name
    request.data['post'] = comment.post.id
    serialized_comment = CommentSerializer(comment, data = request.data)
    if serialized_comment.is_valid():
      serialized_comment.save()
      return Response(serialized_comment.data)
    else:
      return Response(serialized_comment.errors)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request):
    comment_pk = request.data['comment_pk']
    comment = Comment.objects.get(pk=comment_pk)

    comment.delete()
    return Response('DELORTED')


#-- Stuff for friends --


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friend_requests(request):
   requests = FriendInvite.objects.all()
   requests_serialized = FriendInviteSerializer(requests, many=True)
   return Response(requests_serialized.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_friend_request(request):
    sender = Profile.objects.get(pk = request.data['sender'])
    reciever = Profile.objects.get(pk = request.data['reciever'])
    if FriendInvite.objects.filter(sender = sender, reciever = reciever).exists() or reciever in sender.friends.all():
       return Response('already')
    else:
      friend_request = FriendInvite.objects.create (
         sender = sender,
         reciever = reciever
      )
      serialized_friend_request = FriendInviteSerializer(friend_request, data=request.data)
      if serialized_friend_request.is_valid():
         serialized_friend_request.save()
         return Response(serialized_friend_request.data)
      return Response(serialized_friend_request.errors)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request):
   print(request.data['request'])
   friend_request = FriendInvite.objects.get(pk = request.data['request'])
   sender = Profile.objects.get(pk = friend_request.sender.pk)
   reciever = Profile.objects.get(pk = friend_request.reciever.pk)

   sender.friends.add(reciever)
   reciever.friends.add(sender)

   friend_request.delete()

   profiles = Profile.objects.all()
   all_profiles_serializer = ProfileSerializer(profiles, many=True)
   return Response(all_profiles_serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request):
   request_pk = request.data['request']
   friend_request = FriendInvite.objects.get(pk = request_pk)

   friend_request.delete()
   return Response('no frienderino')

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def delete_friend(request):
   user = Profile.objects.get(pk = request.data['user'])
   friend = Profile.objects.get(pk = request.data['friend'])

   user.friends.remove(friend)
   friend.friends.remove(user)

   profiles = Profile.objects.all()
   all_profiles_serializer = ProfileSerializer(profiles, many=True)
   return Response(all_profiles_serializer.data)

#-- Stuff for groups --


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_groups(request):
   groups = Group.objects.all()
   groups_serialized = GroupSerializer(groups, many=True)
   return Response(groups_serialized.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
   creator_pk = request.data['creator']
   founder = Profile.objects.get(pk = creator_pk)

   group = Group.objects.create (
      name = request.data['name'],
      founder = founder,
   )
   group.group_admin.set([founder.pk])
   group.members.set([founder.pk])

   serialized_group = GroupSerializer(group, data=request.data)
   if serialized_group.is_valid():
      serialized_group.save()
      return Response(serialized_group.data)
   return Response(serialized_group.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_invites(request):
   group_invites = GroupInvite.objects.all()
   group_invites_serialized = GroupInviteSerializer(group_invites, many=True)
   return Response(group_invites_serialized.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_to_group(request):
   group = Group.objects.get(pk = request.data['group'])
   user_being_invited = request.data['invited_user']
   invited_user = Profile.objects.get(pk = user_being_invited)

   if GroupInvite.objects.filter(group = group, invited_user = invited_user).exists() or invited_user in group.members.all():
       return Response('already')
   else:
      invite = GroupInvite.objects.create (
         group = group,
         invited_user = invited_user
      )

      serialized_invite = GroupInviteSerializer(invite, data = request.data)
      if serialized_invite.is_valid():
         serialized_invite.save()
         return Response(serialized_invite.data)
      return Response(serialized_invite.errors)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_group_invite(request):
   invite = GroupInvite.objects.get(pk = request.data['invite'])
   group = Group.objects.get(pk = invite.group.id)

   group.members.add(invite.invited_user)

   invite.delete()

   serialized_group = GroupSerializer(group, data = request.data)
   if serialized_group.is_valid():
      serialized_group.save()
      return Response(serialized_group.data)
   return Response(serialized_group.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reject_group_invite(request):
   invite_pk = request.data['invite']
   invite = GroupInvite.objects.get(pk = invite_pk)

   invite.delete()
   return Response('no grouperino')

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def kick_from_group(request):
   group_pk = request.data['group']
   group = Group.objects.get(pk = group_pk)
   member_to_kick = request.data['member_to_kick']
   group.members.remove(member_to_kick)

   serialized_group = GroupSerializer(group, data = request.data)
   if serialized_group.is_valid():
      serialized_group.save()
      return Response(serialized_group.data)
   return Response(serialized_group.errors)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_join_request(request):
   group = Group.objects.get(pk = request.data['group'])
   user_pk = request.data['user']
   user = Profile.objects.get(pk = user_pk)

   if GroupJoinRequest.objects.filter(group = group, sender = user).exists() or user in group.members.all():
       return Response('already')
   else:
      join_request = GroupJoinRequest.objects.create (
         group = group,
         sender = user,
      )

      serialized_request = GroupInviteSerializer(join_request, data = request.data)
      if serialized_request.is_valid():
         serialized_request.save()
         return Response(serialized_request.data)
      return Response(serialized_request.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_join_requests(request):
   join_requests = GroupJoinRequest.objects.all()
   join_requests_serialized = GroupJoinRequestSerializer(join_requests, many=True)
   return Response(join_requests_serialized.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_join_request(request):
   join_request = GroupJoinRequest.objects.get(pk = request.data['request'])
   group = Group.objects.get(pk = join_request.group.id)

   group.members.add(join_request.sender)

   join_request.delete()

   serialized_group = GroupSerializer(group, data = request.data)
   if serialized_group.is_valid():
      serialized_group.save()
      return Response(serialized_group.data)
   return Response(serialized_group.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reject_join_request(request):
   request_pk = request.data['request']
   join_request = GroupJoinRequest.objects.get(pk = request_pk)

   join_request.delete()
   return Response('no joinerino')

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def leave_group(request):
   group = Group.objects.get(pk = request.data['group'])
   member = Profile.objects.get(pk = request.data['member_leaving'])

   group.members.remove(member)
   serialized_group = GroupSerializer(group, data = request.data)
   if serialized_group.is_valid():
      serialized_group.save()
      return Response(serialized_group.data)
   return Response(serialized_group.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def dissolve_group(request):
   group = Group.objects.get(pk = request.data['group'])

   group.delete()

   return Response('rip in pepperonis mate')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request):
   messages = GroupMessage.objects.all()
   messages_serialized = GroupMessageSerializer(messages, many=True)
   return Response(messages_serialized.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
   group_pk = request.data['group']
   message_group = Group.objects.get(pk = group_pk)

   sender_pk = request.data['sender']
   message_sender = Profile.objects.get(pk = sender_pk)
   
   message = GroupMessage.objects.create(
      group = message_group,
      sender = message_sender,
      text_content = request.data['text_content'],
   )

   message_serialized = GroupMessageSerializer(message, data=request.data)
   if message_serialized.is_valid():
      message_serialized.save()
      return Response(message_serialized.data)
   return Response(message_serialized.errors)


# -- stuff for friend DMs --

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_dm(request):
  sender_id = request.data['sender']
  sender = Profile.objects.get(id=sender_id)
  reciever_id = request.data['reciever']
  reciever = Profile.objects.get(id=reciever_id)
  

  
  message = FriendMessage.objects.create (
    sender = sender,
    reciever = reciever,
    text_content = request.data['text_content'],
  )

  serialized_message = FriendMessageSerializer(message, data=request.data)
  if serialized_message.is_valid():
    serialized_message.save()
    return Response(serialized_message.data)
  return Response(serialized_message.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
@parser_classes([MultiPartParser, FormParser])
def get_dms(request):
  messages = FriendMessage.objects.all()
  messages_serialized = FriendMessageSerializer(messages, many=True)
  return Response(messages_serialized.data)