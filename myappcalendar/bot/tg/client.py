import time

import marshmallow_dataclass
import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from bot.tg.functions import get_bot_data


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        try:
            url = self.get_url('getUpdates')
            data = requests.get(url=f'{url}?offset={offset}&timeout={timeout}').json()
            GetUpdatesSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
            data_object = get_bot_data(data=data, schema=GetUpdatesSchema)
            return data_object
        except RuntimeError:
            print("Caught NotImplementedError via RuntimeError")
            raise NotImplementedError

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        try:
            url = self.get_url('sendMessage')
            time.sleep(1)
            data = requests.get(url=f'{url}?chat_id={chat_id}&text={text}').json()
            SendMessageSchema = marshmallow_dataclass.class_schema(SendMessageResponse)
            data_object = get_bot_data(data=data, schema=SendMessageSchema)
            return data_object
        except RuntimeError:
            print("Caught NotImplementedError via RuntimeError")
            raise NotImplementedError

    def send_dice(self, chat_id: int, message_id: int = None, emoji: str = "") -> SendMessageResponse:
        try:
            url = self.get_url('sendDice')
            time.sleep(1)
            data = requests.get(
                url=f'{url}?chat_id={chat_id}&emoji={emoji}&reply_to_message_id={message_id}').json()
            SendMessageSchema = marshmallow_dataclass.class_schema(SendMessageResponse)
            data_object = get_bot_data(data=data, schema=SendMessageSchema)
            return data_object
        except RuntimeError:
            print("Caught NotImplementedError via RuntimeError")
            raise NotImplementedError


# offset = 0
# tg_client = TgClient("5418285199:AAEh5o1ZOC_q1HuVmayAirf36WEOZ27VhyQ")
# while True:
#     res = tg_client.get_updates(offset=offset)
#     for item in res.result:
#         offset = item.update_id + 1
#         chat_id = item.message.chat.id
#         reply_to_message_id = item.message.message_id
#         tg_client.send_dice(chat_id=chat_id, emoji='🎯')
# while True:
#     res = tg_client.get_updates(offset=offset)
#     for item in res.result:
#         offset = item.update_id + 1
#         print(item.message)
