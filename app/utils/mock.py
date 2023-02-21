import json
import typing as tp

from sqlalchemy.orm import Session


from app.schemas.customer import CustomerCreate, CustomerDB
from app.schemas.product import ProductDB, ProductBase
from app.schemas.purchase import PurchaseCreate
from app.database import crud


def read_json(path: str) -> dict:
    with open(path, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data


def write_mock_data(db: Session) -> None:
    try:
        customers: tp.List[CustomerCreate] = read_json(r"app\database\mock\customers.json")
        products: tp.List[CustomerCreate] = read_json(r"app\database\mock\products.json")

        db_customers: tp.List[str] = []
        for customer in customers:
            new_customer = CustomerCreate(**customer)
            db_customer: CustomerDB = crud.customer.create_customer(db, new_customer)
            db_customers.append(db_customer.uuid)

        db_products: tp.List[ProductDB] = []
        for product in products:
            new_product = ProductBase(**product)
            db_product = crud.product.create_product(db, new_product)
            db_products.append(db_product)

        # add purchases for 1st customer
        purchases = [
            {
                "purchase_date": "2023-02-16",
                "customer_uuid": db_customers[0],
                "purchase_products": [
                    {
                        "product_id": db_products[0].id,
                        "count": 4,
                        "product_cost": db_products[0].selling_price,
                        "summary_cost": round(db_products[0].selling_price * 4, 2)
                    },
                    {
                        "product_id": db_products[1].id,
                        "count": 7,
                        "product_cost": db_products[1].selling_price,
                        "summary_cost": round(db_products[1].selling_price * 7, 2)
                    }
                ]
            },
            {
                "purchase_date": "2023-02-17",
                "customer_uuid": db_customers[0],
                "purchase_products": [
                    {
                        "product_id": db_products[0].id,
                        "count": 2,
                        "product_cost": db_products[0].selling_price,
                        "summary_cost": round(db_products[0].selling_price * 2, 2)
                    },
                    {
                        "product_id": db_products[2].id,
                        "count": 3,
                        "product_cost": db_products[2].selling_price,
                        "summary_cost": round(db_products[2].selling_price * 3, 2)
                    }
                ]
            }
        ]
        for purchase in purchases:
            new_purchase = PurchaseCreate(**purchase)
            crud.purchase.create_purchase(db, new_purchase)

        # add purchases for 1st customer
        purchases = [
            {
                "purchase_date": "2023-02-16",
                "customer_uuid": db_customers[1],
                "purchase_products": [
                    {
                        "product_id": db_products[2].id,
                        "count": 10,
                        "product_cost": db_products[2].selling_price,
                        "summary_cost": round(db_products[2].selling_price * 10, 2)
                    },
                    {
                        "product_id": db_products[1].id,
                        "count": 2,
                        "product_cost": db_products[1].selling_price,
                        "summary_cost": round(db_products[1].selling_price * 2, 2)
                    }
                ]
            },
            {
                "purchase_date": "2023-02-19",
                "customer_uuid": db_customers[1],
                "purchase_products": [
                    {
                        "product_id": db_products[0].id,
                        "count": 20,
                        "product_cost": db_products[0].selling_price,
                        "summary_cost": round(db_products[0].selling_price * 20, 2)
                    },
                    {
                        "product_id": db_products[2].id,
                        "count": 13,
                        "product_cost": db_products[2].selling_price,
                        "summary_cost": round(db_products[2].selling_price * 13, 2)
                    }
                ]
            }
        ]
        for purchase in purchases:
            new_purchase = PurchaseCreate(**purchase)
            crud.purchase.create_purchase(db, new_purchase)
    except Exception:
        db.rollback()
