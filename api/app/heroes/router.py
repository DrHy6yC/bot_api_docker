from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Depends

from sqlmodel import select

from api.app.auth.auth_bearer import JWTBearer
from api.app.db import SessionDep
from api.app.schemas import HeroPublic, HeroCreate, Hero, HeroUpdate


router = APIRouter(
    prefix="/heroes",
    tags=["Герои"],
    dependencies=[Depends(JWTBearer())]
)

@router.post(
    path="/",
    response_model=HeroPublic,
    dependencies=[Depends(JWTBearer())]
)
async def create_hero(
        hero: HeroCreate,
        session: SessionDep
) -> Hero:
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    await session.commit()
    await session.refresh(db_hero)
    return db_hero


@router.get(
    path="/",
    response_model=list[HeroPublic],
    dependencies=[Depends(JWTBearer())]
)
async def read_heroes(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> list[HeroPublic]:
    heroes = (await session.execute(select(Hero).offset(offset).limit(limit))).scalars().all()
    return heroes


@router.get(
    path="/{hero_id}",
    response_model=HeroPublic,
    dependencies=[Depends(JWTBearer())]
)
async def read_hero(
        hero_id: int,
        session: SessionDep
) -> HeroPublic:
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=404,
            detail="Hero not found"
        )
    return hero


@router.patch(
    path="/{hero_id}",
    response_model=HeroPublic,
    dependencies=[Depends(JWTBearer())]
)
async def update_hero(
        hero_id: int,
        hero: HeroUpdate,
        session: SessionDep
) -> HeroPublic:
    hero_db = await session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(
            status_code=404,
            detail="Hero not found"
        )
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    await session.commit()
    await session.refresh(hero_db)
    return hero_db

#TODO: Добавить тип возвращаемых данных, создать схему для сообщения об успешном удалении
@router.delete(
    path="/{hero_id}",
    dependencies=[Depends(JWTBearer())]
)
async def delete_hero(
        hero_id: int,
        session: SessionDep
)-> dict:
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=404,
            detail="Hero not found"
        )
    await session.delete(hero)
    await session.commit()
    return {"ok": True}