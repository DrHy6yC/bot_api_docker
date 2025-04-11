from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from api.app.config import templates, our_url

router = APIRouter(
    prefix="/profiles",
    tags=["Профили"],
)


@router.get(
    path="/",
    response_class=HTMLResponse
)
async def not_profile(
        request: Request
) -> HTMLResponse:
    context = {"url": our_url}
    return templates.TemplateResponse(
        name="not_profile.html",
        context=context,
        request=request
    )


@router.get(
    path="/{user_login}",
    response_class=HTMLResponse
)
async def user_profile(
        request: Request,
        user_login: str
) -> HTMLResponse:
    #TODO загрузка данных из БД
    context = {"url": our_url, "user_login": user_login}
    return templates.TemplateResponse(
        name="profile.html",
        context=context,
        request=request
    )