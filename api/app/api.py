from yandexid import YandexOAuth, YandexID
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, WebSocket, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.websockets import WebSocketDisconnect

from sqlmodel import select

from api.app.db import create_db_and_tables, SessionDep
from api.app.schemas import HeroPublic, HeroCreate, Hero, HeroUpdate
from api.app.config import client_id, client_secret, redirect_uri, refs, our_url


@asynccontextmanager
async def lifespan(apps: FastAPI):
    print("Api запущен")
    yield
    print("Api выключен")


app = FastAPI(lifespan=lifespan, title="Api DB")


templates = Jinja2Templates(directory="api/app/templates")

yandex_oauth = YandexOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )

@app.get(path="/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context=refs)


@app.websocket(path="/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
        except WebSocketDisconnect as e:
            print(f"WebSocket disconnected: {e}")
            break


@app.get(path="/login")
async def login(request: Request):
    auth_url = yandex_oauth.get_authorization_url()
    print(auth_url)
    return RedirectResponse(auth_url)


@app.get(path="/token")
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


@app.get(path="/profile", response_class=HTMLResponse)
async def not_profile(request: Request):
    context = {"url": our_url}
    return templates.TemplateResponse(
        name="not_profile.html",
        context=context,
        request=request
    )


@app.get(path="/profile/{user_login}", response_class=HTMLResponse)
async def user_profile(request: Request, user_login: str):
    #TODO загрузка данных из БД
    context = {"url": our_url, "user_login": user_login}
    return templates.TemplateResponse(
        name="profile.html",
        context=context,
        request=request
    )

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.post(path="/heroes/", response_model=HeroPublic)
async def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    await session.commit()
    await session.refresh(db_hero)
    return db_hero


@app.get(path="/heroes/", response_model=list[HeroPublic])
async def read_heroes(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = (await session.execute(select(Hero).offset(offset).limit(limit))).scalars().all()
    return heroes


@app.get(path="/heroes/{hero_id}", response_model=HeroPublic)
async def read_hero(hero_id: int, session: SessionDep):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch(path="/heroes/{hero_id}", response_model=HeroPublic)
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


@app.delete(path="/heroes/{hero_id}")
async def delete_hero(hero_id: int, session: SessionDep):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    await session.delete(hero)
    await session.commit()
    return {"ok": True}
