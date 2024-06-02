from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    tg_id: int
    full_name: str
    username: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    tg_id: int | None = None
    full_name: str | None = None
    username: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
