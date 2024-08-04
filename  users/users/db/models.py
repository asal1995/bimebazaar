from sqlalchemy import Column, Integer, String, Boolean, Enum

from users.db.database import Base
from users.db.enums import USerTypeEnum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='true')
    type_ = Column(Enum(USerTypeEnum), nullable=False, server_default=USerTypeEnum.USER.name)

    def __repr__(self):
        return f"<User email={self.email} active={self.is_active}>"

