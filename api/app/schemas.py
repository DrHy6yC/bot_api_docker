from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: str = Field()
    last_name: str = Field()

class UserAuth(UserBase):
    yandex_id: str = Field(unique=True, index=True)

class User(UserAuth, table=True):
    id: int = Field(primary_key=True, index=True)
    display_name: str = Field(index=True)
    picture: str | None = Field(default=None)
    provider: str | None = Field(default=None)

class UserTokenBase(SQLModel):
    access_token: str =Field(primary_key=True, index=True)

class UserToken(UserTokenBase, table=True):
    id: int =Field(primary_key=True, index=True)

#TODO: добавить группу ссылок
class RefBase(SQLModel):
    url: str = Field(index=True)
    target: str

class Ref(RefBase, table=True):
    id: int = Field(primary_key=True, index=True)


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None

