from fastapi import APIRouter, Request

from api.app.config import templates, settings

router = APIRouter(
    prefix="/profiles",
    tags=["Профили"],
)


# TODO: добавить тип возвращаемых данных в аннотации
@router.get("/{profile_id}")
async def current_profile(
        request: Request
):
    token = request.headers.get("authorization")
    # TODO: подтянуть профиль пользователя
    return templates.TemplateResponse(
        name="profile.html",
        request=request,
        context={
            "url": settings.OUR_URL,
            "token": token
        }
    )
