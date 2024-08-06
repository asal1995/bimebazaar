from typing import Union

from pydantic import BaseModel, ConfigDict

from bcr.db.enums import RatingEnum
from bcr.db.models import CommentRating


class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CommentRateCreate(MyModel):
    book_id: int
    comment: Union[str, None]
    rate: Union[str, None]


class CommentRatingSchema(MyModel):
    user_id: int
    book_id: int
    rating: RatingEnum = None
    comment: str = None


class UserCommentsRatings(BaseModel):
    user_id: int
    comments_rating: list[CommentRatingSchema]


class BookStats(BaseModel):
    book_id: int
    comments_count: int
    ratings_count: int
    average_rating: float
    ratings_distribution: dict[int, int]
    user_comments_ratings: list[UserCommentsRatings]
