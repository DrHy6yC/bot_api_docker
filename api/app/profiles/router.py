from fastapi import APIRouter

router = APIRouter(
    prefix="/profiles",
    tags=["Профили"],
)

@router.get("/{profile_id}")
async def current_profile():
    pass