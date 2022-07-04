import pprint

import requests
from pathlib import Path

from bot.tg.tg_test_data import tg_test_data, test_sendMessage_data
url1 = 'https://api.telegram.org/bot5418285199:AAEh5o1ZOC_q1HuVmayAirf36WEOZ27VhyQ/getUpdates'
url2 =f'https://api.telegram.org/bot5418285199:AAEh5o1ZOC_q1HuVmayAirf36WEOZ27VhyQ/sendMessage?chat_id=220018112&text=&parse_mode=Markdown'
url3 ='https://api.telegram.org/bot5418285199:AAEh5o1ZOC_q1HuVmayAirf36WEOZ27VhyQ/sendDice?chat_id=220018112}&emoji=🎯'
data = requests.get(url=url1).json()
pprint.pprint(data)

# BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)
