from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    purchase_cost: float
    selling_price: float


class ProductDB(ProductBase):
    id: int

    class Config:
        orm_mode = True
