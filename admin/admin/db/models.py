from sqlalchemy import Column, Integer, String, Boolean, Enum, Float

from admin.db.database import Base
from admin.db.enums import Role


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    type_ = Column(Enum(Role), nullable=False)
