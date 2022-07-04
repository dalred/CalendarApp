from dataclasses import dataclass, field
from typing import List
from marshmallow import EXCLUDE



# @dataclass
# class GetUpdatesResponse:
#     ok: bool
#     result: List[UpdateObj]  # todo
#
#     class Meta:
#         unknown = EXCLUDE


@dataclass
class TelegramMessageChat:
    id: int = 0
    first_name: str = None
    last_name: str = None
    username: str = None
    type: str = None


@dataclass
class TelegramMessageFrom:
    id: int = 0
    is_bot: bool = False
    first_name: str = None
    last_name: str = None
    username: str = None
    language_code: str = None


@dataclass
class Message:
    from_: TelegramMessageFrom = field(default_factory=TelegramMessageFrom, metadata={"data_key": "from"})
    chat: TelegramMessageChat = field(default_factory=TelegramMessageChat)
    date: int = 0
    text: str = None
    message_id: int = 0
    entities: list = None  # [{"offset":0,"length":5,"type":"bot_command"}]

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    message: Message
    update_id: int = 0



@dataclass
class GetUpdatesResponse:
    ok: bool
    result: list[UpdateObj] = field(default_factory=list[UpdateObj])


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE



