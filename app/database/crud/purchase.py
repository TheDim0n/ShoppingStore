import typing as tp

from sqlalchemy.orm import Session


from app.schemas import purchase
from app.schemas.purchase_product import PurchaseProductCreate
from app.database.models import Purchase, PurchaseProduct


def create_purchase(db: Session, new_purchase: purchase.PurchaseCreate) -> Purchase:
    db_purchase = Purchase(
        customer_uuid=new_purchase.customer_uuid,
        purchase_date=new_purchase.purchase_date
    )
    db.add(db_purchase)
    db.flush([db_purchase])
    for purchase_product in new_purchase.purchase_products:
        db_product = PurchaseProduct(
            purchase_id=db_purchase.id,
            **purchase_product.dict()
        )
        db.add(db_product)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def read_purchases(db: Session) -> tp.List[Purchase]:
    return db.query(Purchase).all()


def get_purchase_by_id(db: Session, id: int) -> Purchase:
    return db.query(Purchase).filter_by(id=id).first()


def update_purchase_products_by_id(
    db: Session,
    id: int,
    products: tp.List[PurchaseProductCreate]
) -> Purchase:
    try:
        db_purchase = db.query(Purchase).filter_by(id=id).first()
        db.query(PurchaseProduct).filter_by(purchase_id=id).delete()
        for product in products:
            db_product = PurchaseProduct(
                purchase_id=id,
                **product.dict()
            )
            db.add(db_product)
        db.commit()
        db.refresh(db_purchase)
        return db_purchase.products
    except Exception:
        db.rollback()


def remove_purchase_by_uuid(db: Session, id: int) -> None:
    db_purchase = get_purchase_by_id(db=db, id=id)
    db.delete(db_purchase)
    db.commit()
