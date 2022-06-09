import json

from django.contrib.auth import logout as logout_user
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse

from users.serializers import UserListSerializer, UserCreateSerializer, UserCurrentSerializer, ChangePasswordSerializer


def root(request: WSGIRequest) -> JsonResponse:
    return JsonResponse({
        "status": "ok"
    })


User = get_user_model()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]


class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    # Можно тут проверить
    # def post(self, request, *args, **kwargs):
    #     password = request.data.get('password')
    #     password_repeat = request.data.get('password_repeat')
    #     if password != password_repeat:
    #         raise serializers.ValidationError("passwords must match!")
    #     else:
    #         request.data.pop('password_repeat')
    #         return self.create(request, *args, **kwargs)


class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCurrentSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        # Предполагаю что фронт берет один объект, если несколько то без .get() and many=True
        serializer = self.serializer_class(self.request.user, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user, data=request.data, many=False, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    # TODO не знаю как сделать корректно
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user, data=request.data, many=False, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePassword(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return JsonResponse({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return JsonResponse(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO не знаю как разделить put и patch бред тут какой-то одно поле тут меняется и все
    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return JsonResponse({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return JsonResponse(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)