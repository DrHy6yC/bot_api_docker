from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from auth365.schemas import OAuth2Callback

from api.app.auth.auth_handler import sign_jwt
from api.app.config import yandex_oauth
from api.app.schemas import UserToken

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post(
    path="/login"
)
async def login_in_yandex() -> RedirectResponse:
    async with yandex_oauth:
        url = await yandex_oauth.get_authorization_url()
        return RedirectResponse(url=url)

@router.get(
    path="/token",
    response_model=UserToken
)
async def oauth_callback(callback: Annotated[OAuth2Callback, Depends()]) -> dict[str, Exception] | UserToken:
    try:
        async with yandex_oauth:
            # TODO: Добавить статус код для ошибки авторизации
            await yandex_oauth.authorize(callback)
            user = await yandex_oauth.userinfo()
            token = sign_jwt(user.id)
            return token
    except Exception as e:
        print(e)
        return {"error": e}
