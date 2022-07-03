from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField()
    tg_id = serializers.SlugField(source='telegram_chat_id', read_only=True)

    class Meta:
        model = TgUser
        fields = ('username', 'user_id', 'verification_code', 'tg_id')
        read_only_fields = ('username', 'user_id', 'tg_id')

    def validate(self, data):
        verification_code = data.get('verification_code')
        self._tg_user = TgUser.objects.filter(verification_code=verification_code).first()
        if not self._tg_user:
            raise serializers.ValidationError({"verification_code": "verification code is incorrect"})
        data['tg_user'] = self._tg_user
        return data