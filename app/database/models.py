import uuid


from sqlalchemy import Column, String, Integer, Date, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.sql.functions import now

from app.database.database import DataBase
from app.utils import enums


class User(DataBase):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)


class Customer(DataBase):
    __tablename__ = "customer"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=False)
    registration_date = Column(Date, nullable=False, default=now())
    pd_consent = Column(Boolean, nullable=False)
    photo_url = Column(String, nullable=True)
    sex = Column(ENUM(enums.Sex, name="sex", create_type=False), nullable=True)


class Product(DataBase):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    purchase_cost = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
