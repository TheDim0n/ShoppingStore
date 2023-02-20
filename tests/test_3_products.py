from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from httpx import Response

from app.database.database import DataBase
from app.dependencies import get_db, get_settings
from app.main import app

from tests.common import get_access_token

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

test_product_id: int | None = None


def test_product_post_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    test_product = {
        "name": "test product",
        "purchase_cost": 1000,
        "selling_price": 1200.5,
    }
    response: response = client.post("/products", json=test_product, headers=headers)
    assert response.status_code == 201

    global test_product_id
    test_product_id = response.json()["id"]
    assert test_product_id is not None



def test_products_get_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response: Response = client.get("/products", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_products_put_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    new_product_data = {
        "name": "test product",
        "purchase_cost": 1000,
        "selling_price": 1500,
    }

    global test_product_id
    response: response = client.put(
        f"/products/{test_product_id}",
        json=new_product_data, headers=headers
    )
    assert response.status_code == 201
    assert response.json()["name"] == "test product"
    assert response.json()["selling_price"] == 1500


def test_product_delete_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    global test_product_id
    response = client.delete(f"/products/{test_product_id}", headers=headers)
    assert response.status_code == 204
