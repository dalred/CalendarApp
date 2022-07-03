from typing import Union

import marshmallow
from marshmallow import Schema
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse

def get_bot_data(data: dict, schema: Schema) -> Union[GetUpdatesResponse, SendMessageResponse]:
    try:
        return schema().load(data)
    except marshmallow.exceptions.ValidationError:
        raise ValueError