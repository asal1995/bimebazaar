from pydantic import BaseModel


class MyModel(BaseModel):
    class Config:
        orm_mode = True


class BookCreate(MyModel):
    title: str
    author: str
    description: str
