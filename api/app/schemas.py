from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: str = Field()
    last_name: str = Field()


class User(UserBase, table=True):
    id: int = Field(primary_key=True, index=True)
    yandex_id: str = Field(unique=True, index=True)
    display_name: str = Field(index=True)
    picture: str | None = Field(default=None)
    provider: str | None = Field(default=None)

#TODO: добавить группу ссылок
class Ref(SQLModel, table=True):
    url: str = Field(primary_key=True, index=True)
    target: str


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
