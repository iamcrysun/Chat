from pydantic import BaseModel

from server.controller.schemas.entity import EntityDBSchema


class ChattingDBSchema(EntityDBSchema):
    question: str
    answer: str
    user_id: int

    class Config:
        from_attributes = True


class ChattingCreateSchema(BaseModel):
    question: str
    answer: str

