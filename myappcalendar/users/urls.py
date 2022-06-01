from django.urls import path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views
from rest_framework.authtoken import views
import users

urlpatterns = [
    path('users/', users.views.UserListAPIView.as_view()),
    path('users/<int:pk>/', users.views.UserRetrieveView.as_view()),
    path('users/signup/', users.views.UserCreate.as_view()),
    # path('login/', views.obtain_auth_token),
    re_path(r'^login/?$', TokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view())
]
