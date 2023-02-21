from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.database import crud
from app.dependencies import get_db
from app.schemas import purchase
from app.schemas.purchase import PurchaseProductDB, PurchaseProductCreate
from app.utils import auth


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"],
    dependencies=[Depends(auth.get_current_user)]
)


@router.get("", summary="Read purchases")
async def read_purchases(db=Depends(get_db)) -> List[purchase.PurchaseDB]:
    purchases: List[purchase.PurchaseDB] = crud.purchase.read_purchases(db)
    if not purchases:
        raise HTTPException(status_code=404)
    return purchases


@router.get("/{id}", summary="Read purchase by ID")
async def read_purchase(id: int, db=Depends(get_db)) -> purchase.PurchaseDB:
    purchase: purchase.PurchaseDB = crud.purchase.get_purchase_by_id(db, id)
    if not purchase:
        raise HTTPException(status_code=404)
    return purchase



@router.post("", status_code=201, summary="Create new user")
async def create_purchases(
    new_purchase: purchase.PurchaseCreate,
    db=Depends(get_db)
) -> purchase.PurchaseDB:
    return crud.purchase.create_purchase(db=db, new_purchase=new_purchase)


@router.delete("/{id}", status_code=204, summary="Remove purchase by ID")
async def remove_purchase(id: int, db=Depends(get_db)):
    crud.purchase.remove_purchase_by_uuid(db, id)


@router.put("/{id}/products", status_code=201, summary="Update purchase's products")
async def update_purchase_products(
    id: int,
    products: List[PurchaseProductCreate],
    db=Depends(get_db)
) -> List[PurchaseProductDB]:
    return crud.purchase.update_purchase_products_by_id(db, id, products)
    return db_purchase.products
