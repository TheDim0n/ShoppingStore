import typing as tp

from sqlalchemy.orm import Session


from app.schemas import customer
from app.database.models import Customer


def create_customer(db: Session, new_customer: customer.CustomerCreate) -> Customer:
    db_customer = Customer(**new_customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def read_customers(db: Session) -> tp.List[Customer]:
    return db.query(Customer).all()


def get_customer_by_uuid(db: Session, uuid: str) -> Customer:
    return db.query(Customer).filter_by(uuid=uuid).first()


def remove_customer_by_uuid(db: Session, uuid: str) -> None:
    db_customer = get_customer_by_uuid(db=db, uuid=uuid)
    db.delete(db_customer)
    db.commit()


def update_cutomer_by_uuid(db: Session, uuid: str, data: customer.CustomerBase) -> None:
    db.query(Customer).filter_by(uuid=uuid).update(data.dict())
    db.commit()
    return get_customer_by_uuid(db, uuid)
