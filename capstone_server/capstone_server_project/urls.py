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
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)