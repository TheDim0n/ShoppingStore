from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.models import User
from app.schemas.token import Token, TokenData
from app.dependencies import get_db
from app.utils import auth


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/token",
    status_code=201,
    response_model=Token,
    summary="Get access token for user",
)
async def get_user_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user_db: User = auth.authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user_db:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth.create_token_pair(
        TokenData(user=user_db), response=response
    )


@router.post(
    "/refresh",
    status_code=201,
    response_model=Token,
    summary="Refresh user's access token",
)
async def refresh_token(
    response: Response, request: Request, db: Session = Depends(get_db)
):
    refresh = request.cookies.get("refresh")
    if not refresh:
        raise HTTPException(status_code=401)
    user_db: User = auth.get_current_user(token=refresh, db=db)
    return auth.create_token_pair(
        TokenData(user=user_db), response=response
    )
