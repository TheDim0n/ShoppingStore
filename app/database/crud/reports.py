import typing as tp
import sqlalchemy as sa

from datetime import date
from sqlalchemy.orm import Session


from app.database import models
from app.schemas import reports


def get_customer_sum_report(
    db: Session,
    start_date: str = None,
    end_date: str = None
):
    purchases = db.query(
        models.Purchase.purchase_date.label("purchase_date"),
        models.Purchase.id.label("purchase_id"),
        models.Customer.uuid.label("uuid")
    )\
    .select_from(models.Purchase)\
    .join(models.Customer, models.Customer.uuid == models.Purchase.customer_uuid)\


    if start_date:
        purchases = purchases.filter(models.Purchase.purchase_date >= start_date)

    if end_date:
        criterion: bool = models.Purchase.purchase_date <= date.fromisoformat(end_date)
        purchases = purchases.filter(criterion)

    purchases = purchases.subquery("purchases")

    report = db.query(
        purchases.c.uuid.label("uuid"),
        sa.func.sum(models.PurchaseProduct.summary_cost).label("sum")
    )\
    .select_from(purchases)\
    .join(
        models.PurchaseProduct,
        purchases.c.purchase_id == models.PurchaseProduct.purchase_id
    )\
    .group_by(purchases.c.uuid).subquery("report")

    return db.query(
        models.Customer.uuid,
        models.Customer.full_name,
        sa.func.coalesce(report.c.sum, 0).label("sum")
    )\
    .select_from(models.Customer)\
    .join(report, report.c.uuid == models.Customer.uuid, isouter=True)\
    .all()
