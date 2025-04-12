import time
import jwt

from api.app.config import settings
from api.app.schemas import UserToken


def token_response(token: str) -> UserToken:
    return UserToken(access_token=token)


def sign_jwt(user_name: str) -> UserToken:
    expires = time.time() + float(settings.TOKEN_LIFETIME)
    payload = {
        "user_name": user_name,
        "expires": expires
    }
    print(payload)
    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
