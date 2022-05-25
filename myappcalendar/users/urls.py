from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views

import users

urlpatterns = [
    path('users/', users.views.UserListAPIView.as_view()),
    path('users/<int:pk>/', users.views.UserRetrieveView.as_view()),
    path('users/create/', users.views.UserCreate.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
]