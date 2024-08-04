from pydantic import BaseModel, ConfigDict

from bcr.db.enums import RatingEnum


class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RatingCreate(MyModel):
    user_id: int
    book_id: int
    rating: RatingEnum


class Rating(MyModel):
    id: int
    user_id: int
    book_id: int
    rating: RatingEnum
