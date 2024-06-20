from django.contrib import admin
from capstone_server_app.models import *


class ProfileAdmin(admin.ModelAdmin):
  pass

class ImageAdmin(admin.ModelAdmin):
  pass

class ForumPostAdmin(admin.ModelAdmin):
  pass

class CommentAdmin(admin.ModelAdmin):
  pass

class GroupAdmin(admin.ModelAdmin):
  pass

class FriendInviteAdmin(admin.ModelAdmin):
  pass

class GroupInviteAdmin(admin.ModelAdmin):
  pass

class GroupJoinRequestAdmin(admin.ModelAdmin):
  pass

class GroupMessageAdmin(admin.ModelAdmin):
  pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ForumPost, ForumPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(FriendInvite, FriendInviteAdmin)
admin.site.register(GroupInvite, GroupInviteAdmin)
admin.site.register(GroupJoinRequest, GroupJoinRequestAdmin)
admin.site.register(GroupMessage, GroupMessageAdmin)