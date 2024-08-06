from sqlalchemy import Column, Integer, String, Boolean, Enum, Float

from books.db.database import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String)
    ave_rate = Column(Float)
    comment_count = Column(Integer, default=0)


