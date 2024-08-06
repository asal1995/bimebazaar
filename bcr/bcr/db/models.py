from sqlalchemy import Column, Integer, String, UniqueConstraint, Enum
from sqlalchemy.ext.declarative import declarative_base

from bcr.db.database import Base
from bcr.db.enums import RatingEnum


class CommentRating(Base):
    __tablename__ = 'comments_rating'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    book_id = Column(Integer, nullable=False)
    rating = Column(Enum(RatingEnum), nullable=True)
    comment = Column(String, nullable=True)
    __table_args__ = (UniqueConstraint('user_id', 'book_id', name='_user_book_uc'),)


class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    book_id = Column(Integer, nullable=False)
