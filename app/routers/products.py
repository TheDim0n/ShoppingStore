from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.database import crud
from app.dependencies import get_db
from app.schemas import product
from app.utils import auth


router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(auth.get_current_user)]
)


@router.get("", summary="Read products")
async def read_products(db=Depends(get_db)) -> List[product.ProductDB]:
    products: List[product.ProductDB] = crud.product.read_products(db)
    if not products:
        raise HTTPException(status_code=404)
    return products


@router.post("", status_code=201, summary="Create new user")
async def create_product(
    new_product: product.ProductBase,
    db=Depends(get_db)
) -> product.ProductDB:
    return crud.product.create_product(db=db, new_product=new_product)


@router.put("/{id}", status_code=201)
async def update_product(
    id: int,
    data: product.ProductBase,
    db=Depends(get_db)
) -> product.ProductDB:
    return crud.product.update_product_by_id(db, id, data)


@router.delete("/{id}", status_code=204)
async def remove_product(id: int, db=Depends(get_db)):
    crud.product.remove_product_by_id(db, id)
