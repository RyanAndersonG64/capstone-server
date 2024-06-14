from django.contrib import admin
from capstone_server_app.models import *


class ProfileAdmin(admin.ModelAdmin):
  pass

class ImageAdmin(admin.ModelAdmin):
  pass

class ForumPostAdmin(admin.ModelAdmin):
  pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ForumPost, ForumPostAdmin)