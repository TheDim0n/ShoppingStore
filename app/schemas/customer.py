from datetime import date
from pydantic import BaseModel
from uuid import UUID

from app.utils import enums


class CustomerBase(BaseModel):
    full_name: str
    birth_year: int
    registration_date: date
    pd_consent: bool
    photo_url: str | None = None
    sex: enums.Sex | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerDB(CustomerBase):
    uuid: UUID | str

    class Config:
        orm_mode = True
