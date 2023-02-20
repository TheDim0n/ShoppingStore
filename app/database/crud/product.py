import typing as tp

from sqlalchemy import update
from sqlalchemy.orm import Session


from app.schemas import product
from app.database.models import Product


def create_product(db: Session, new_product: product.ProductBase) -> Product:
    db_product = Product(**new_product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def read_products(db: Session) -> tp.List[Product]:
    return db.query(Product).all()


def update_product_by_id(db: Session, id: int, data: product.ProductBase) -> Product:
    db_product = db.query(Product).filter_by(id=id).update(data.dict())
    db.commit()
    return get_product_by_id(db, id)


def get_product_by_id(db: Session, id: int) -> Product:
    return db.query(Product).filter_by(id=id).first()


def remove_product_by_id(db: Session, id: int) -> None:
    db_product = get_product_by_id(db=db, id=id)
    db.delete(db_product)
    db.commit()
