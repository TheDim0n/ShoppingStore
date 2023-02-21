from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.database import crud
from app.dependencies import get_db
from app.schemas import user
from app.utils import auth


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(auth.get_current_user)]
)


@router.get("", summary="Read users")
async def read_users(db=Depends(get_db)) -> List[user.UserDB]:
    users: List[user.UserDB] = crud.user.read_users(db)
    if not users:
        raise HTTPException(status_code=404)
    return users


@router.post("", status_code=201, summary="Create new user")
async def create_user(new_user: user.UserCreate,
                      db=Depends(get_db)) -> user.UserDB:
    db_user = crud.user.get_user_by_login(db, new_user.login)
    if db_user:
        return db_user
    return crud.user.create_user(db=db, new_user=new_user)


@router.delete("/{uuid}", status_code=204)
async def remove_user(uuid: str, db=Depends(get_db)):
    crud.user.remove_user_by_uuid(db, uuid)
