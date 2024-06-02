from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    full_name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorCreate):
    pass


class AuthorUpdatePartial(AuthorCreate):
    full_name: str | None = None


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
