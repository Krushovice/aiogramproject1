from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    tg_id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    usernname: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    tg_id: int | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
