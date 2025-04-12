from fastapi import APIRouter, Response, status

from api.app.auth.auth_handler import sign_jwt
from api.app.schemas import UserTokenBase, UserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Автиоризация"],
)

@router.post(
    path="/register"
)
async def create_user(
        response: Response,
        user: UserAuth
) -> UserTokenBase:
    # TODO: Запись данных пользователя в БД
    token = sign_jwt(user.yandex_id)
    return token



@router.post(
    path="/login"
)
async def user_login(
        response: Response,
        user: UserAuth
) -> UserTokenBase:
    # TODO Проверка данных пользователя на соответствие в БД
    token = sign_jwt(user.yandex_id)
    response.status_code = status.HTTP_200_OK
    return token