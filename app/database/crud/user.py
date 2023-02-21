import typing as tp

from sqlalchemy.orm import Session


from app.schemas import user
from app.database.models import User


def create_user(db: Session, new_user: user.UserCreate) -> User:
    db_user = User(login=new_user.login, hashed_password=new_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_users(db: Session) -> tp.List[User]:
    return db.query(User).all()


def get_user_by_login(db: Session, login: str) -> User:
    return db.query(User).filter_by(login=login).first()


def get_user_by_uuid(db: Session, uuid: str) -> User:
    return db.query(User).filter_by(uuid=uuid).first()


def remove_user_by_uuid(db: Session, uuid: str) -> None:
    db_user = get_user_by_uuid(db=db, uuid=uuid)
    db.delete(db_user)
    db.commit()
