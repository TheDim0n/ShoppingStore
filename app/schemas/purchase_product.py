from pydantic import BaseModel


from app.schemas.product import ProductDB


class PurchaseProductBase(BaseModel):
    count: int
    product_cost: float
    summary_cost: float


class PurchaseProductCreate(PurchaseProductBase):
    product_id: int


class PurchaseProductDB(PurchaseProductBase):
    product: ProductDB

    class Config:
        orm_mode = True
