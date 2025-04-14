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
        return f"{self.OUR_URL}{self.REDIRECT_YANDEX}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

templates = Jinja2Templates(directory="api/app/templates")

# TODO: Перенести эти ссылки в БД
refs_nav = [
    Ref(url=f'{settings.OUR_URL}/docs#', target='Swagger'),
    Ref(url='https://github.com/DrHy6yC', target='Мой Git'),
    Ref(url='https://krasnodar.hh.ru/resume/46d175e3ff08684f230039ed1f564366383552', target='Резюме на hh.ru'),

]

refs_body = [
    Ref(url=f'{settings.OUR_URL}/docs#', target='Посмотреть документацию API'),
    Ref(url=f'{settings.OUR_URL}/create_db', target='Создать таблицы в БД'),
    Ref(url=f'{settings.OUR_URL}/auth/login', target='Получить токен используя УЗ Яндекса'),
]

refs = {
    'refs_nav': refs_nav,
    'refs_body': refs_body
}
