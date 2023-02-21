from typing import List

from datetime import date
from pydantic import BaseModel
from uuid import UUID


from app.schemas.customer import CustomerDB
from app.schemas.purchase_product import PurchaseProductCreate, PurchaseProductDB


class PurchaseBase(BaseModel):
    purchase_date: date


class PurchaseCreate(PurchaseBase):
    customer_uuid: UUID | str
    purchase_products: List[PurchaseProductCreate]


class PurchaseDB(PurchaseBase):
    id: int
    customer: CustomerDB
    products: List[PurchaseProductDB]

    class Config:
        orm_mode = True
