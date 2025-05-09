from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from api.app.auth.auth_bearer import JWTBearer
from api.app.config import refs, settings, templates
from api.app.db import create_db_and_tables

from api.app.auth.router import router as auth_router
from api.app.heroes.router import router as heroes_router
from api.app.profiles.router import router as profiles_router


@asynccontextmanager
async def lifespan(apps: FastAPI):
    print("Api запущен")
    yield
    print("Api выключен")


app = FastAPI(lifespan=lifespan, title="Api DB")

app.include_router(auth_router)
app.include_router(profiles_router)
app.include_router(heroes_router)

app.mount(
    path='/static',
    app=StaticFiles(directory='api/app/static'),
    name='static')


@app.get(
    path="/",
    response_class=HTMLResponse
)
async def index_page(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context=refs)


@app.get(
    path="/create_db",
    dependencies=[Depends(JWTBearer())]
)
async def create_db():
    await create_db_and_tables()
    return RedirectResponse(settings.OUR_URL)
