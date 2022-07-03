from django.core.management.base import BaseCommand
import os

from bot.models import TgUser
from bot.tg.client import TgClient


class Command(BaseCommand):
    help = "runbot command"
    tg_client = TgClient(os.environ.get('TOKEN_BOT'))

    @property
    def _generate_code(self) -> str:
        return os.urandom(12).hex()

    def verification_code(self, tg_chat_id, tg_user):
        code = self._generate_code
        tg_user.verification_code = code
        tg_user.save(update_fields=['verification_code'])
        self.tg_client.send_message(
            chat_id=tg_chat_id,
            text=f'verification_code is {code}'
        )

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                # user_id = item.message.from_.id
                tg_chat_id = item.message.chat.id
                tg_message_id = item.message.message_id
                tg_username = item.message.from_.username
                # TgUser_exists = TgUser.objects.filter(telegram_chat_id=tg_chat_id).exists()
                tg_user, created = TgUser.objects.get_or_create(
                    telegram_chat_id=tg_chat_id,
                    defaults={
                        'username': tg_username,
                        'telegram_chat_id': tg_chat_id
                    }
                )
                if created:
                    self.tg_client.send_message(chat_id=tg_chat_id, text='Приветствую друг!')
                    self.verification_code(tg_chat_id=tg_chat_id, tg_user=tg_user)
                elif not tg_user.user:
                    self.verification_code(tg_chat_id=tg_chat_id, tg_user=tg_user)
                elif tg_user.user:
                    self.tg_client.send_message(chat_id=tg_chat_id, text=f'Пообщаемся {tg_username}!!!')
                    self.tg_client.send_dice(chat_id=tg_chat_id, emoji='🎯', message_id=tg_message_id)
