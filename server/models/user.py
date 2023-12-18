from sqlalchemy import Column, String

from server.models.entity import Entity


class User(Entity):
    __tablename__ = "users"

    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
