from django.urls import path, re_path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from django.views.decorators.csrf import csrf_exempt
from users import views
import users

urlpatterns = [
    path('users/', users.views.UserListAPIView.as_view()),
    re_path(r'^profile/?$', csrf_exempt(users.views.UserRetrieveUpdateDestroy.as_view())),
    re_path(r'^update_password/?$', csrf_exempt(users.views.UpdatePassword.as_view())),
    # re_path(r'^profile/test/?$', users.views.UserRetrieveUpdateView.as_view()),
    # re_path(r'profile/<int:pk>', users.views.UserRetrieveUpdateView.as_view()),
    re_path(r'^signup/?$', users.views.UserCreate.as_view()),
    # path('login/', views.obtain_auth_token),
    # re_path(r'^login/?$', TokenObtainPairView.as_view()),
    # path('login/refresh/', TokenRefreshView.as_view())
]
