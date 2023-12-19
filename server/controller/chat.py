from typing import List, Type

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from server.controller.auth import get_current_user
from server.logic.result import qa_bert
from server.models.chatting import Chatting
from server.schemas.chatting import ChattingDBSchema
from server.utils import db
from server.utils.db import get_db

router = APIRouter(prefix="/chat")


class Answer(BaseModel):
    message: str


class Question(BaseModel):
    message: str


@router.get('/')
def items(db=Depends(get_db)):
    return db.query(Chatting).all()


@router.get('/all/', response_model=List[ChattingDBSchema])
async def chatting_by_user(current_user=Depends(get_current_user)) -> Type[Chatting]:
    """
    Chatting by user
    """
    return db.query(Chatting).filter(current_user.id == Chatting.person_id).all()


@router.post('/', response_model=Answer)
def answer(question: Question,
           current_user=Depends(get_current_user),
           db=Depends(get_db)) -> Answer:
    message = question.message
    bert_answer = qa_bert(message)
    chatting = Chatting(
        user_id=current_user.id,
        question=message,
        answer=bert_answer,
    )
    db.add(chatting)
    db.commit()
    return Answer(message=bert_answer)
