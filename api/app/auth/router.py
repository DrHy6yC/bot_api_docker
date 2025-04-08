from yandexid import YandexID

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from api.app.config import our_url, yandex_oauth

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.get(path="/token")
async def get_token(request: Request, code: str, cid: str):
    print(request.query_params)
    try:
        token = yandex_oauth.get_token_from_code(code)
        # TODO отправлять в headers авторизацию
        yandex_id = YandexID(token.access_token)
        user_info = yandex_id.get_user_info_json()
        print(user_info)
        profile_url = f"{our_url}/profile/{cid}"
        #TODO добавить отпарвку в БД данных о клиенте
    except Exception as e:
        print(e)
        profile_url = f"{our_url}/profile"
    return RedirectResponse(profile_url)


@router.get(path="/login")
async def login(request: Request):
    auth_url = yandex_oauth.get_authorization_url()
    print(auth_url)
    return RedirectResponse(auth_url)