from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from httpx import Response

from app.database.database import DataBase
from app.dependencies import get_db, get_settings
from app.main import app

from tests.common import get_headers

settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False, bind=engine)

DataBase.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app, base_url="http://localhost")

test_purchase_id: int | None = None
test_product_id: int | None = None
test_customer_uuid: str | None = None


TEST_CUSTOMER = {
    "full_name": "Customer 1",
    "birth_year": 1980,
    "registration_date": "2023-02-20",
    "pd_consent": 1,
    "sex": "М"
}

TEST_PRODUCT = {
    "name": "test product",
    "purchase_cost": 1000,
    "selling_price": 1200.5,
}


def test_purchases_post_method():
    headers = get_headers(
        client, settings.initial_user_username, settings.initial_user_password
    )

    response: Response = client.post("/customers", json=TEST_CUSTOMER, headers=headers)
    assert response.status_code == 201
    global test_customer_uuid
    test_customer_uuid = response.json()["uuid"]

    response: Response = client.post("/products", json=TEST_PRODUCT, headers=headers)
    assert response.status_code == 201
    global test_product_id
    test_product_id = response.json()["id"]

    test_purchase = {
        "purchase_date": "2023-02-20",
        "customer_uuid": test_customer_uuid,
        "purchase_products": [{
            "product_id": test_product_id,
            "count": 4,
            "product_cost": TEST_PRODUCT["selling_price"],
            "summary_cost": TEST_PRODUCT["selling_price"] * 4
        }]
    }

    response: response = client.post("/purchases", json=test_purchase, headers=headers)
    assert response.status_code == 201

    global test_purchase_id
    test_purchase_id = response.json()["id"]
    assert test_purchase_id is not None
    assert len(response.json()["products"]) == 1
    assert response.json()["products"][0]["product"]["name"] == "test product"


def test_purchases_get_list_method():
    headers = get_headers(
        client, settings.initial_user_username, settings.initial_user_password
    )

    response: Response = client.get("/purchases", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_purchases_get_by_id_method():
    headers = get_headers(
        client, settings.initial_user_username, settings.initial_user_password
    )

    global test_purchase_id
    response: Response = client.get(f"/purchases/{test_purchase_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == test_purchase_id


def test_purchases_put_method():
    headers = get_headers(
        client, settings.initial_user_username, settings.initial_user_password
    )

    global test_product_id
    new_product_data = [{
        "product_id": test_product_id,
        "count": 10,
        "product_cost": TEST_PRODUCT["selling_price"],
        "summary_cost": TEST_PRODUCT["selling_price"] * 10
    }]

    global test_purchase_id
    response: Response = client.put(
        f"/purchases/{test_purchase_id}/products",
        json=new_product_data, headers=headers
    )
    assert response.status_code == 201
    assert len(response.json()) == 1
    assert response.json()[0]["count"] == 10
    assert response.json()[0]["product"]["id"] == test_product_id


def test_purchases_delete_method():
    headers = get_headers(
        client, settings.initial_user_username, settings.initial_user_password
    )

    global test_purchase_id
    response:Response = client.delete(f"/purchases/{test_purchase_id}", headers=headers)
    assert response.status_code == 204

    response: Response = client.get(f"/purchases/{test_purchase_id}", headers=headers)
    assert response.status_code == 404
