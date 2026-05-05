from pydantic import BaseModel
from datetime import datetime


class OutboundProgressObject(BaseModel):
    level: int
    level_xp: int
    streak: int
    answered_questions: int
    questions_correct: int
    questions_incorrect: int
    updated_at: datetime
    created_at: datetime


class OutboundProgressResponse(BaseModel):
    items: list[OutboundProgressObject]
