import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from .database import DataBase


class User(DataBase):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
