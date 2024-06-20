from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)
from capstone_server_app.views import *
from django.conf import settings
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework import routers
from capstone_server_app.views import *

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', get_profile),
    path('refresh/', TokenRefreshView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('get-profile/', get_profile),
    path('create-user/', create_user),
    path('add-credit/', add_credit),
    path('remove-credit/', remove_credit),
    path('set-favorite/', set_favorite),
    path('get-all-users/', get_all_users),
    path('add-post/', add_post),
    path('get-posts/', get_posts),
    path('edit-post/', edit_post),
    path('delete-post/', delete_post),
    path('like-post/', like_post),
    path('create-image/', create_image),
    path('get-images/', get_images),
    path('delete-image/', delete_image),
    path('like-image/', like_image),
    path('add-comment/', add_comment),
    path('get-comments/', get_comments),
    path('edit-comment/', edit_comment),
    path('delete-comment/', delete_comment),
    path('create-friend-request/', create_friend_request),
    path('get-friend-requests/', get_friend_requests),
    path('accept-friend-request/', accept_friend_request),
    path('reject-friend-request', reject_friend_request),
    path('get-groups/', get_groups),
    path('create-group/', create_group),
    path('get-group-invites/', get_group_invites),
    path('invite-to-group/', invite_to_group),
    path('accept-group-invite/', accept_group_invite),
    path('reject-group-invite/', reject_group_invite),
    path('kick-from-group/', kick_from_group),
    path('get-join-requests/', get_join_requests),
    path('create-join-request/', create_join_request),
    path('accept-join-request/', accept_join_request),
    path('reject-join-request/', reject_join_request),
    path('get-messages/', get_messages),
    path('send-message/', send_message),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)