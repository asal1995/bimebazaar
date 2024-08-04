from pydantic import BaseModel, ConfigDict


class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CommentCreate(MyModel):
    user_id: int
    book_id: int
    comment: str


class Comment(MyModel):
    id: int
    user_id: int
    book_id: int
    comment: str
