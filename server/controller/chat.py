from fastapi import APIRouter, Depends
from pydantic import BaseModel

from server.controller.auth import get_current_user
from server.logic.result import qa_bert
from server.models.chatting import Chatting
from server.utils.db import get_db

router = APIRouter(prefix="/chat")


class Answer(BaseModel):
    message: str


class Question(BaseModel):
    message: str


@router.get('/')
def items(db = Depends(get_db)):
    return db.query(Chatting).all()

@router.post('/', response_model=Answer)
def answer(question: Question,
           current_user = Depends(get_current_user),
           db = Depends(get_db)) -> Answer:
    message = question.message
    bert_answer=qa_bert(message)
    chatting = Chatting(
        user_id=current_user.id,
        question=message,
        answer=message,
    )
    db.add(chatting)
    db.commit()
    # do smt with message
    return Answer(message=bert_answer)
