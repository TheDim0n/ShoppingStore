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

test_user_uuid: str = ''


def test_user_get_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response: Response = client.get("/users", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_user_post_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    test_user = {"login": "test", "password": "test", "full_name": "Test User"}
    response: response = client.post("/users", json=test_user, headers=headers)
    assert response.status_code == 201

    global test_user_uuid
    test_user_uuid = response.json()["uuid"]
    assert test_user_uuid is not None


def test_user_delete_method():
    access_token = get_access_token(
        client, settings.initial_user_username, settings.initial_user_password
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    test_user = {"login": "test", "password": "test", "full_name": "Test User"}
    response = client.delete(f"/users/{test_user_uuid}", headers=headers)
    assert response.status_code == 204
