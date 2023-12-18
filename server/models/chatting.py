from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from server.models.entity import Entity


class Chatting(Entity):
    __tablename__ = "chatting"

    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    user = relationship("User", backref="users")
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
