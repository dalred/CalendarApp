import pprint

import requests


class BaseBot:
    def __init__(self, token):
        self.token = token
        self.session = requests.session()


url = 'https://api.telegram.org/bot5418285199:AAEh5o1ZOC_q1HuVmayAirf36WEOZ27VhyQ/getMe'
url1 = 'https://api.telegram.org/bot5418285199:AAEh5o1ZOC_q1HuVmayAirf36WEOZ27VhyQ/getUpdates'
pprint.pprint(requests.get(url=url1).json())


