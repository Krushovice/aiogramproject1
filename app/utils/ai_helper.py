# import uuid
# import json
# import aiohttp
# import requests
# import certifi
# import urllib3
# from requests.auth import HTTPBasicAuth
#
# from core import settings
#
#
# class AiHelper:
#     def __init__(self) -> None:
#         self.session = aiohttp.ClientSession()
#         self.id = settings.ai_id
#         self.secret = settings.ai_secret
#         self.auth = settings.auth
#
#     async def __aenter__(self):
#         self.session = aiohttp.ClientSession()
#         return self
#
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         await self.session.close()
#
#     async def close(self):
#         await self.session.close()
#
#     async def create_token(self):
#         url = f"https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
#         payload = {'scope': "GIGACHAT_API_PERS"}
#         headers = {
#             'Content-Type': 'application/x-www-form-urlencoded',
#             'Accept': 'application/json',
#             'RqUID': str(uuid.uuid4()),
#             'Authorization': f'Basic {self.auth}'
#         }
#
#         async with self.session.post(
#                 url,
#                 headers=headers,
#                 data=payload,) as response:
#             res = await response.json()
#             return res.json()["access_token"]
#
#     async def send_prompt(self, token: str, message: str, stream=False,):
#         url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
#
#         payload = json.dumps({
#             "model": "GigaChat",
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": f"{message}"
#                 }
#             ]})
#         headers = {
#             'Content-Type': 'application/json',
#             'Accept': 'application/json',
#             'Authorization': f'Bearer {token}'
#         }
#
#         async with self.session.post(
#                 url,
#                 headers=headers,
#                 data=payload,
#                 stream=stream,
#         ) as response:
#             response = await response.json()
#             return response["choices"][0]["message"]["content"]
#
#
# ai_helper = AiHelper()


import requests
from requests.auth import HTTPBasicAuth
import json
import uuid
from core import settings
import threading


class SyncHelper:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(SyncHelper, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.id = settings.ai_id
        self.secret = settings.ai_secret

    def create_token(self) -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        payload = {"scope": "GIGACHAT_API_PERS"}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
        }

        res = requests.post(
            url=url,
            headers=headers,
            auth=HTTPBasicAuth(self.id, self.secret),
            data=payload,
            verify=False,  # Отключение проверки сертификата
            timeout=5,
        )

        res.raise_for_status()  # Вызывает исключение для статусов ошибок
        access_token = res.json()["access_token"]
        return access_token

    def send_prompt(self, token: str, message: str) -> str:
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

        res = requests.post(
            url=url,
            headers=headers,
            json=payload,  # Использование параметра json для автоматического преобразования в JSON
            verify=False,  # Отключение проверки сертификата
        )

        res.raise_for_status()  # Вызывает исключение для статусов ошибок
        return res.json()["choices"][0]["message"]["content"][:1024]


sync_helper = SyncHelper()
