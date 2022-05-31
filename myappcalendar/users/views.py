from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from users.serializers import UserListSerializer, UserCreateSerializer

def root(request: WSGIRequest) -> JsonResponse:
    return JsonResponse({
        "status": "ok"
    })


User = get_user_model()
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer