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

test_customer_uuid: str = ''


def test_customer_post_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    test_customer = {
        "full_name": "Tester Testerov Testerovich",
        "birth_year": 2000,
        "registration_date": "2023-02-20",
        "pd_consent": 1,
        "sex": "М"
    }
    response: response = client.post("/customers", json=test_customer, headers=headers)
    assert response.status_code == 201

    global test_customer_uuid
    test_customer_uuid = response.json()["uuid"]
    assert test_customer_uuid is not None



def test_customer_get_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response: Response = client.get("/customers", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_customer_put_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    new_customer_data = {
        "full_name": "Tester Testerov Testerovich",
        "birth_year": 2000,
        "registration_date": "2023-02-20",
        "pd_consent": 0,
        "sex": "М"
    }

    global test_customer_uuid
    response: response = client.put(f"/customers/{test_customer_uuid}", json=new_customer_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["birth_year"] == 2000
    assert response.json()["pd_consent"] == 0


def test_customer_delete_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    global test_customer_uuid
    response = client.delete(f"/customers/{test_customer_uuid}", headers=headers)
    assert response.status_code == 204
