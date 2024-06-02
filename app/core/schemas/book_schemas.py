from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    name: str
    description: str
    genre: str


class BookCreate(BookBase):
    pass


class BookUpdate(BookCreate):
    pass


class BookUpdatePartial(BookCreate):
    name: str | None = None
    description: str | None = None
    genre: str | None = None


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
