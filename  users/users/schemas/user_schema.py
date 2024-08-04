from pydantic import BaseModel, EmailStr, ConfigDict


class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(MyModel):
    email: EmailStr
    password: str
