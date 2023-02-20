import typing as tp

from pydantic import BaseModel

from app.schemas.user import UserDB


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user: UserDB
