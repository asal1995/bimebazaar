from pydantic import BaseModel, ConfigDict


class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BookCreate(MyModel):
    title: str
    author: str
    description: str


class BookUpdate(MyModel):
    title: str
    author: str
    description: str


class Book(MyModel):
    id: int
    title: str
    author: str
    description: str
    comment_count: int
