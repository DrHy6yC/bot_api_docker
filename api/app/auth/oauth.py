from typing import Annotated

from auth365.providers.yandex import YandexOAuth
from auth365.schemas import OAuth2Callback, OpenID

from fastapi import  Depends

from api.app.config import settings


yandex_oauth = YandexOAuth(
    client_id=settings.YANDEX_CLIENT_ID,
    client_secret=settings.YANDEX_CLIENT_SECRET,
    redirect_uri=settings.REDIRECT_URI,
)


async def get_yandex_auth_url() -> str:
    async with yandex_oauth:
        url = await yandex_oauth.get_authorization_url()
        return url

async def get_yandex_user_info(
        callback: Annotated[OAuth2Callback, Depends()]
) -> OpenID:
    async with yandex_oauth:
        await yandex_oauth.authorize(callback)
        user = await yandex_oauth.userinfo()
        return user