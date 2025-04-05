from os import getenv
from dotenv import load_dotenv

from api.app.schemas import Ref

load_dotenv()

client_id = getenv('CLIENT_ID')
client_secret = getenv('CLIENT_SECRET')
our_url = getenv('OUR_URL')
redirect_us_uri = getenv('REDIRECT_YANDEX')
redirect_uri = f'{our_url}/{redirect_us_uri}'

refs_nav = [
    Ref(url=f'{our_url}/docs#', target='Swagger'),
    Ref(url='https://github.com/DrHy6yC', target='Мой Git'),
    Ref(url='https://krasnodar.hh.ru/resume/46d175e3ff08684f230039ed1f564366383552', target='Резюме на hh.ru'),
    Ref(url=f'{our_url}/login', target='Авторизоваться через Яндекс'),
]


refs_body = [
    Ref(url=f'{our_url}/docs#', target='Посмотреть документацию API'),
    Ref(url='https://github.com/DrHy6yC', target='Попасть на мой Git'),
    Ref(url='https://krasnodar.hh.ru/resume/46d175e3ff08684f230039ed1f564366383552', target='Найти резюме классного специалиста'),
]

refs = {
    'refs_nav': refs_nav,
    'refs_body': refs_body
}