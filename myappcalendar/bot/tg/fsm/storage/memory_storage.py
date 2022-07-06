from enum import Enum, unique, auto
from typing import Dict, Optional
from dataclasses import dataclass, field
import marshmallow_dataclass
from bot.tg.fsm.storage.base import Storage



@dataclass
class NewGoal:
    goal_title: str = None
    cat_id: int = 0

    def complete(self) -> bool:
        return None not in {self.cat_id, self.goal_title}

@unique
class StateEnum(Enum):
    CREATE_CATEGORY_STATE = auto()
    HAS_CHOSEN_CATEGORY = auto()
    GET_GOALS = auto()

@dataclass
class StorageData:
    state: StateEnum = None
    data: dict = field(default_factory=dict)


class MemoryStorage(Storage):

    def __init__(self):
        self.data: dict[int, StorageData] = {}

    def _resolve_chat(self, chat_id: int) -> StorageData:
        if chat_id not in self.data:
            self.data[chat_id] = StorageData()
        return self.data[chat_id]

    def get_all_data(self, chat_id: int) -> StorageData:
        return self._resolve_chat(chat_id)

    def get_state(self, chat_id: int) -> Optional[Enum]:
        return self._resolve_chat(chat_id).state

    def get_data(self, chat_id: int) -> dict:
        return self._resolve_chat(chat_id).data

    def set_state(self, chat_id: int, state: Enum) -> None:
        self._resolve_chat(chat_id).state = state

    def set_data(self, chat_id: int, data: dict) -> None:
        self._resolve_chat(chat_id).data = data

    def reset_state(self, chat_id: int) -> None:
        self._resolve_chat(chat_id).state = None

    def reset_data(self, chat_id: int) -> None:
        self._resolve_chat(chat_id).data.clear()

    def update_data(self, chat_id: int, **kwargs) -> None:
        self._resolve_chat(chat_id).data.update(**kwargs)

    # /cancel
    def reset(self, chat_id: int) -> bool:
        return bool(self.data.pop(chat_id, None))

# storage = MemoryStorage()
# storage.set_data(chat_id=123, data=NewGoal(cat_id=1).__dict__)
# cat_id = storage.get_data(chat_id=123).get('cat_id')
# goal = NewGoal(goal_title='111111', cat_id=cat_id)
# print(**goal)
# # data = storage.get_data(chat_id=123)
# # data['goal_title'] = '2ssss'
# # storage.set_data(chat_id=123, data=data)
# # print(storage.get_data(chat_id=123))