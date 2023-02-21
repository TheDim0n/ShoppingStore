from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.database import crud
from app.dependencies import get_db
from app.schemas import customer
from app.utils import auth


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[Depends(auth.get_current_user)]
)


@router.get("", summary="Read customers")
async def read_customers(db=Depends(get_db)) -> List[customer.CustomerDB]:
    customers: List[customer.CustomerDB] = crud.customer.read_customers(db)
    if not customers:
        raise HTTPException(status_code=404)
    return customers


@router.post("", status_code=201, summary="Create new customer")
async def create_customer(
    new_customer: customer.CustomerCreate,
    db=Depends(get_db)
) -> customer.CustomerDB:
    return crud.customer.create_customer(db=db, new_customer=new_customer)


@router.put("/{uuid}", status_code=201)
async def update_customer(
    uuid: str,
    customer_data: customer.CustomerBase,
    db=Depends(get_db)
) -> customer.CustomerDB:
    db_customer = crud.customer.update_cutomer_by_uuid(db, uuid, customer_data)
    return db_customer


@router.delete("/{uuid}", status_code=204)
async def remove_customer(uuid: str, db=Depends(get_db)) -> None:
    crud.customer.remove_customer_by_uuid(db, uuid)
