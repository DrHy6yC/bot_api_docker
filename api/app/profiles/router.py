from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from auth365.schemas import OAuth2Callback, OpenID

from api.app.config import yandex_oauth

router = APIRouter(
    prefix="/profiles",
    tags=["Профили"],
)

@router.get("/")
async def oauth_callback(callback: Annotated[OAuth2Callback, Depends()]) -> OpenID:
    async with yandex_oauth:
        await yandex_oauth.authorize(callback)
        #TODO: Дбавить генерацию и отправку токена, сохранение пользователя в БД
        return await yandex_oauth.userinfo()


@router.get("/login")
async def login() -> RedirectResponse:
    async with yandex_oauth:
        url = await yandex_oauth.get_authorization_url()
        return RedirectResponse(url=url)


