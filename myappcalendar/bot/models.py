from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TgUser(models.Model):
    telegram_chat_id = models.IntegerField(verbose_name="tg_chat_id")
    username = models.CharField(max_length=255, blank=True, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, null=True)
    verification_code = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Код верификации")
    # chat_id и user_id может совпасть
    # telegram_user_id = models.IntegerField(verbose_name="tg_user_id")


    class Meta:
        verbose_name = 'Telegram Пользователь'
        verbose_name_plural = 'Telegram Пользователи'
        ordering = ("id",)
