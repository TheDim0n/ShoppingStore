from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import DataBase
from app.dependencies import get_db, get_settings
from app.main import app



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


def test_clear_initial_db():
    DataBase.metadata.drop_all(bind=engine)
    DataBase.metadata.create_all(bind=engine)
    assert len(DataBase.metadata.tables.keys()) > 0


def test_startup_user_success():
    with TestClient(app) as cl:
        payload = "password={}&username={}".format(
            settings.initial_user_username, settings.initial_user_password
        )
        response = cl.post(
            "/auth/token",
            content=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 201
        assert response.json()["access_token"]
