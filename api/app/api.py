from typing import Annotated
from contextlib import asynccontextmanager
from urllib.parse import urlencode

from fastapi import FastAPI, WebSocket, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.websockets import WebSocketDisconnect

from sqlmodel import select

from api.app.db import create_db_and_tables, SessionDep
from api.app.schemas import HeroPublic, HeroCreate, Hero, HeroUpdate
from api.app.config import clientID, redirect_us_uri


@asynccontextmanager
async def lifespan(apps: FastAPI):
    print("Api запущен")
    yield
    print("Api выключен")


app = FastAPI(lifespan=lifespan, title="Api DB")


templates = Jinja2Templates(directory="api/app/templates")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
        except WebSocketDisconnect as e:
            print(f"WebSocket disconnected: {e}")
            break


@app.get("/login")
async def login(request: Request):
    client_id = clientID
    redirect_uri = redirect_us_uri  # Замените на ваш URL
    query = urlencode({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid",

    })
    return RedirectResponse(f"https://oauth.yandex.ru/authorize?{query}")


@app.get("/callback")
async def callback(request: Request, code: str):
    # Здесь будет обработка полученного кода авторизации
    return templates.TemplateResponse("callback.html", {"request": request, "code": code})


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.post("/heroes/", response_model=HeroPublic)
async def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    await session.commit()
    await session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroPublic])
async def read_heroes(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = (await session.execute(select(Hero).offset(offset).limit(limit))).scalars().all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
async def read_hero(hero_id: int, session: SessionDep):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
async def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = await session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    await session.commit()
    await session.refresh(hero_db)
    return hero_db


@app.delete("/heroes/{hero_id}")
async def delete_hero(hero_id: int, session: SessionDep):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    await session.delete(hero)
    await session.commit()
    return {"ok": True}
