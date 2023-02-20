from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.utils import password as passwd
from app.database import crud, models
from app.dependencies import get_settings, get_db
from app.schemas.token import TokenData
from app.schemas.user import UserDB

ALGORITHM = "HS256"

settings = get_settings()

user_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.root_path}/auth/token", scheme_name="Authenticate users"
)


def authenticate_user(db: Session, username: str, password: str) -> models.User:
    user_db = crud.user.get_user_by_login(db=db, login=username)
    if not user_db:
        return False
    if not passwd.verify(password, user_db.hashed_password):
        return False
    return user_db


def create_token(token_data: TokenData, expires_delta: timedelta) -> str:
    data = token_data.dict().copy()
    data["user"]["uuid"] = str(data["user"]["uuid"])
    expire = datetime.utcnow() + expires_delta
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_token_pair(token_data: TokenData, response: Response) -> dict:
    # create access token
    access_token_expires = timedelta(
        minutes=get_settings().access_token_expires_minutes
    )
    access_token = create_token(
        token_data=token_data, expires_delta=access_token_expires
    )

    # create refresh token
    refresh_token_expires = timedelta(days=get_settings().refresh_token_expires_days)
    refresh_token = create_token(
        token_data=token_data, expires_delta=refresh_token_expires
    )
    response.set_cookie(
        key="refresh",
        value=refresh_token,
        expires=int(refresh_token_expires.total_seconds()),
        secure=True,
        httponly=True,
        samesite="strict",
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(
    token: str = Depends(user_oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserDB:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        uuid = payload.get("user")["uuid"]
        if uuid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_db = crud.user.get_user_by_uuid(db=db, uuid=uuid)
    if user_db is None:
        raise credentials_exception
    return user_db
