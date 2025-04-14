from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from auth365.schemas import OAuth2Callback

from api.app.auth.auth_handler import sign_jwt
from api.app.auth.oauth import get_yandex_auth_url, get_yandex_user_info
from api.app.config import settings
from api.app.schemas import UserToken

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.get(
    path="/login"
)
async def login_in_yandex() -> RedirectResponse:
    url = await get_yandex_auth_url()
    return RedirectResponse(
        url=url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


@router.get(
    path="/token",
    response_model=UserToken
)
async def get_token_api(
        callback: Annotated[OAuth2Callback, Depends()],
) -> dict[str, Exception] | UserToken:
    user_info = await get_yandex_user_info(callback)
    token = sign_jwt(user_info.id)
    return token

@router.get(
    path="/callback",
)
async def get_profile_yandex(
        callback: Annotated[OAuth2Callback, Depends()],
):
    user_info = await get_yandex_user_info(callback)
    token = sign_jwt(user_info.id)
    print(token)
    response = RedirectResponse(
        url=f"{settings.OUR_URL}/profiles/{user_info.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response