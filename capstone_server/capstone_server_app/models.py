from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  first_name = models.TextField()
  last_name = models.TextField()
  coasters_ridden = models.JSONField(default=list)
  coaster_count = models.IntegerField()
  favorites = models.JSONField(default=["", "", "", "", "", "", "", "", "", ""])

  def save(self, *args, **kwargs):
        # Update coaster_count to be the length of coasters_ridden
        self.coaster_count = len(self.coasters_ridden)
        # Call the original save method
        super().save(*args, **kwargs)

  def __str__(self):
    return self.user.username
  
class Image(models.Model):
  title = models.TextField(default = '')
  posted_by = models.ForeignKey(Profile, on_delete = models.SET('Deleted User'))
  poster_name = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(upload_to='images/')
  likes = models.ManyToManyField(Profile, related_name = 'image_liked_by')
  liked_by = models.ManyToManyField(Profile, related_name = 'unique_users_who_liked_image', blank=True)

  def __str__(self):
    return self.title
  
class ForumPost(models.Model):
  title = models.TextField(default = 'Untitled Post')
  posted_by = models.ForeignKey(Profile, on_delete = models.SET('Deleted User'))
  poster_name = models.TextField()
  posted_at = models.DateTimeField(auto_now_add=True)
  text_content = models.TextField(max_length=1000)
  likes = models.ManyToManyField(Profile, related_name = 'post_liked_by')
  liked_by = models.ManyToManyField(Profile, related_name = 'unique_users_who_liked_post')
