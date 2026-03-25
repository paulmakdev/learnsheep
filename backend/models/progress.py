from sqlalchemy import Column, String, DateTime, Enum, Boolean, Integer, ForeignKey, Index
import enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Progress(Base):
    __tablename__ = 'progress'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lessons.id'), nullable=False)
    level = Column(Integer, default=0)
    level_progress = Column(Integer, default=0)
    answered_questions = Column(Integer, default=0)
    questions_correct = Column(Integer, default=0)
    questions_incorrect = Column(Integer, default=0)
    understanding_metadata = Column(JSONB)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        # To get per-lesson history and user general history easily
        Index("idx_user_lesson", "user_id", "lesson_id"),

        # If we ever want to get some per-lesson stats
        Index("idx_lesson", "lesson_id")
    )
    

