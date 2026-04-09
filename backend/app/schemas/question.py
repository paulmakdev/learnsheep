from pydantic import BaseModel, UUID4
from app.models.question import Difficulty


class QuestionRequest(BaseModel):
    lesson_id: UUID4
    difficulty: Difficulty


class QuestionResponse(BaseModel):
    question_expression: str
    question_template: dict
    values: dict
    choices: list
    session_token: str


class AnswerRequest(BaseModel):
    answer: str
    session_token: str


class AnswerResponse(BaseModel):
    correct: bool
    new_xp: int
    new_level: int
