from auth365.providers.yandex import YandexOAuth
from pydantic_settings import BaseSettings

from fastapi.templating import Jinja2Templates

from api.app.schemas import Ref


class Settings(BaseSettings):
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    REDIRECT_YANDEX: str
    OUR_URL: str
    JWT_ALGORITHM: str
    JWT_SECRET: str
    TOKEN_LIFETIME: str

    @property
    def REDIRECT_URI(self) -> str:
        return f"{self.OUR_URL}/{self.REDIRECT_YANDEX}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

yandex_oauth = YandexOAuth(
    client_id=settings.YANDEX_CLIENT_ID,
    client_secret=settings.YANDEX_CLIENT_SECRET,
    redirect_uri=settings.REDIRECT_URI,
)

templates = Jinja2Templates(directory="api/app/templates")

refs_nav = [
    Ref(url=f'{settings.OUR_URL}/docs#', target='Swagger'),
    Ref(url='https://github.com/DrHy6yC', target='Мой Git'),
    Ref(url='https://krasnodar.hh.ru/resume/46d175e3ff08684f230039ed1f564366383552', target='Резюме на hh.ru'),
    Ref(url=f'{settings.OUR_URL}/profiles/login', target='Авторизоваться через Яндекс'),
]

refs_body = [
    Ref(url=f'{settings.OUR_URL}/docs#', target='Посмотреть документацию API'),
    Ref(url='https://github.com/DrHy6yC', target='Попасть на мой Git'),
    Ref(url='https://krasnodar.hh.ru/resume/46d175e3ff08684f230039ed1f564366383552',
        target='Найти резюме классного специалиста'),
    Ref(url=f'{settings.OUR_URL}/create_db', target='Создать таблицы в БД'),
]

refs = {
    'refs_nav': refs_nav,
    'refs_body': refs_body
}
