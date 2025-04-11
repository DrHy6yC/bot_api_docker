from yandexid import YandexID
from starlette.websockets import WebSocketDisconnect
from typing import Annotated

from fastapi import Depends, WebSocket
from starlette.responses import RedirectResponse


from auth365.schemas import OAuth2Callback, OpenID

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)

@router.websocket(path="/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
        except WebSocketDisconnect as e:
            print(f"WebSocket disconnected: {e}")
            break

@router.get("/login")
async def login() -> RedirectResponse:
    async with oauth:
        url = await oauth.get_authorization_url()
        return RedirectResponse(url=url)


@router.get("/callback")
async def oauth_callback(callback: Annotated[OAuth2Callback, Depends()]) -> OpenID:
    async with oauth:
        await oauth.authorize(callback)
        print(callback)
        return await oauth.userinfo()

    # @router.get(
    #     path="/",
    #     response_class=HTMLResponse
    # )
    # async def not_profile(
    #         request: Request
    # ) -> HTMLResponse:
    #     context = {"url": settings.OUR_URL}
    #     return templates.TemplateResponse(
    #         name="not_profile.html",
    #         context=context,
    #         request=request
    #     )
    #
    #
    # @router.get(
    #     path="/{user_login}",
    #     response_class=HTMLResponse
    # )
    # async def user_profile(
    #         request: Request,
    #         user_login: str
    # ) -> HTMLResponse:
    #     #TODO загрузка данных из БД
    #     context = {"url": settings.OUR_URL, "user_login": user_login}
    #     return templates.TemplateResponse(
    #         name="profile.html",
    #         context=context,
    #         request=request
    #     )