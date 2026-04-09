from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.question import (
    QuestionRequest,
    QuestionResponse,
    AnswerRequest,
    AnswerResponse,
)
from app.services.question_service import get_question, answer_question
from app.core.database import get_db
from app.core.cache import get_redis, CacheService
from app.core.info import get_current_user

router = APIRouter(prefix="/question", tags=["question"])


@router.get("/ask", response_model=QuestionResponse, status_code=200)
def register(
    data: QuestionRequest = Depends(),
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_redis),
    current_user=Depends(get_current_user),
):
    try:
        return get_question(db, cache, current_user, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/answer", response_model=AnswerResponse, status_code=200)
def login(
    data: AnswerRequest,
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_redis),
    current_user=Depends(get_current_user),
):
    try:
        return answer_question(db, cache, current_user, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
