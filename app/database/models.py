import uuid


from sqlalchemy import Column, String, Integer, Date, Boolean, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
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
    full_name = Column(String, nullable=False, unique=True)
    birth_year = Column(Integer, nullable=False)
    registration_date = Column(Date, nullable=False)
    pd_consent = Column(Boolean, nullable=False)
    photo_url = Column(String, nullable=True)
    sex = Column(ENUM(enums.Sex, name="sex", create_type=False), nullable=True)


class Product(DataBase):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    purchase_cost = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)


class Purchase(DataBase):
    __tablename__ = "purchase"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_uuid = Column(UUID(as_uuid=True), ForeignKey("customer.uuid"),
                           nullable=False)
    purchase_date = Column(Date, nullable=False)

    customer = relationship("Customer")
    products = relationship("PurchaseProduct", cascade="all, delete")


class PurchaseProduct(DataBase):
    __tablename__ = "purchase_product"

    purchase_id = Column(Integer, ForeignKey("purchase.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    count = Column(Integer, nullable=False)
    product_cost = Column(Float, nullable=False)
    summary_cost = Column(Float, nullable=False)

    product = relationship("Product")
