import os

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status

from rest_framework import permissions
from rest_framework.generics import UpdateAPIView

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerView(UpdateAPIView):
    # TODO была идея делать как-то через update внутри сериалайзера но не хватило понимания как это сделать там.
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)  # json -> OrderedDict(десериализация)
        serializer.is_valid(raise_exception=True)
        tg_user = serializer.validated_data.get('tg_user')
        tg_user.user = self.object
        tg_user.save(update_fields=['user'])
        instance_tg_user = self.get_serializer(tg_user)  # Object -> OrderedDict (сериализация)
        tg_client = TgClient(os.environ.get('TOKEN_BOT'))
        tg_client.send_message(chat_id=instance_tg_user.data.get('tg_id'), text="Verification has been completed!")
        return JsonResponse(instance_tg_user.data, status=status.HTTP_204_NO_CONTENT)
