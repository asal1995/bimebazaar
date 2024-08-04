from pydantic import BaseModel, ConfigDict


class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BookmarkCreate(MyModel):
    user_id: int
    book_id: int


class Bookmark(MyModel):
    id: int
    user_id: int
    book_id: int
