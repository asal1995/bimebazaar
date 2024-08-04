from typing import Union

from pydantic import BaseModel, ConfigDict


class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CommentRateCreate(MyModel):
    book_id: int
    comment: Union[str, None]
    rate: Union[str, None]


