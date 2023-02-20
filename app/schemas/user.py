from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class UserDB(UserBase):
    uuid: UUID | str

    class Config:
        orm_mode = True
