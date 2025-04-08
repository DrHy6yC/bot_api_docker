from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.websockets import WebSocketDisconnect


from api.app.auth.router import router as auth_router
from api.app.config import refs, our_url
from api.app.db import create_db_and_tables
from api.app.heroes.router import  router as heroes_router


@asynccontextmanager
async def lifespan(apps: FastAPI):
    print("Api запущен")
    yield
    print("Api выключен")


app = FastAPI(lifespan=lifespan, title="Api DB")


templates = Jinja2Templates(directory="api/app/templates")

app.include_router(auth_router)
app.include_router(heroes_router)

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

@app.get(path="/create_db")
async def create_db():
    await create_db_and_tables()
    return RedirectResponse(our_url)
