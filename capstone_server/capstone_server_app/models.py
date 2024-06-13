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