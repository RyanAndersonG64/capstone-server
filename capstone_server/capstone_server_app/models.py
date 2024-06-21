from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  first_name = models.TextField(max_length=20)
  last_name = models.TextField(max_length=20)
  coasters_ridden = models.JSONField(default=list)
  coaster_count = models.IntegerField()
  favorites = models.JSONField(default=["", "", "", "", "", "", "", "", "", ""])
  friends = models.ManyToManyField('self', blank=True)

  PROFILE_CHOICES = (('PUBLIC', 'Public'), ('PRIVATE', 'Private'), ('FRIENDS ONLY', 'Friends Only'))

  profile_view_state = models.TextField(choices=PROFILE_CHOICES, default = 'Public')

  def save(self, *args, **kwargs):
        # Update coaster_count to be the length of coasters_ridden
        self.coaster_count = len(self.coasters_ridden)
        # Call the original save method
        super().save(*args, **kwargs)

  def __str__(self):
    return self.user.username
  
class Image(models.Model):
  title = models.TextField(max_length=50, default = 'Untitled Image')
  posted_by = models.ForeignKey(Profile, on_delete = models.SET('Deleted User'))
  poster_name = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(upload_to='images/')
  likes = models.ManyToManyField(Profile, related_name = 'image_liked_by')
  liked_by = models.ManyToManyField(Profile, related_name = 'unique_users_who_liked_image', blank=True)

  def __str__(self):
    return self.title
  
class ForumPost(models.Model):
  title = models.TextField(max_length=50, default = 'Untitled Post')
  posted_by = models.ForeignKey(Profile, on_delete = models.SET('Deleted User'))
  poster_name = models.TextField()
  posted_at = models.DateTimeField(auto_now_add=True)
  text_content = models.TextField(max_length=1000)
  likes = models.ManyToManyField(Profile, related_name = 'post_liked_by')
  liked_by = models.ManyToManyField(Profile, related_name = 'unique_users_who_liked_post', blank=True)

class Comment(models.Model):
   post = models.ForeignKey(ForumPost, on_delete = models.CASCADE)
   posted_by = models.ForeignKey(Profile, on_delete = models.SET('Deleted User'))
   poster_name = models.TextField()
   posted_at = models.DateTimeField(auto_now_add=True)
   text_content = models.TextField(max_length=1000)

class Group(models.Model):
   name = models.TextField(max_length = 50)
   founder = models.ForeignKey(Profile, on_delete = models.SET('Deleted User'))
   group_admin = models.ManyToManyField(Profile, related_name = 'group_admin')
   members = models.ManyToManyField(Profile, related_name = 'members')

class FriendInvite(models.Model):
   sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
   reciever = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= 'reciever')

class GroupInvite(models.Model):
   group = models.ForeignKey(Group, on_delete = models.CASCADE)
   invited_user = models.ForeignKey(Profile, on_delete = models.CASCADE)

class GroupJoinRequest(models.Model):
   group = models.ForeignKey(Group, on_delete = models.CASCADE)
   sender = models.ForeignKey(Profile, on_delete = models.CASCADE)

class GroupMessage(models.Model):
   group = models.ForeignKey(Group, on_delete = models.CASCADE)
   sender = models.ForeignKey(Profile, on_delete = models.CASCADE)
   posted_at = models.DateTimeField(auto_now_add=True)
   text_content = models.TextField(max_length=1000)

class FriendMessage(models.Model):
   sender = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='dm_sender')
   reciever = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='dm_reciever')
   text_content = models.TextField(max_length=1000)