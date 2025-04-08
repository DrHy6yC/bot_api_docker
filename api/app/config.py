from os import getenv
from dotenv import load_dotenv
from yandexid import YandexOAuth

from fastapi.templating import Jinja2Templates

from api.app.schemas import Ref

load_dotenv()

templates = Jinja2Templates(directory="api/app/templates")

client_id = getenv('CLIENT_ID')
client_secret = getenv('CLIENT_SECRET')
our_url = getenv('OUR_URL')
redirect_us_uri = getenv('REDIRECT_YANDEX')
redirect_uri = f'{our_url}/{redirect_us_uri}'

yandex_oauth = YandexOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )

refs_nav = [
    Ref(url=f'{our_url}/docs#', target='Swagger'),
    Ref(url='https://github.com/DrHy6yC', target='Мой Git'),
    Ref(url='https://krasnodar.hh.ru/resume/46d175e3ff08684f230039ed1f564366383552', target='Резюме на hh.ru'),
    Ref(url=f'{our_url}/auth/login', target='Авторизоваться через Яндекс'),
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