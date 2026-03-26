from sqlalchemy import Column, String, DateTime, Enum, Boolean, ForeignKey, Index, ForeignKeyConstraint, Integer, UniqueConstraint
import enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Difficulty(enum.Enum):
    EASY = 'easy'
    NORMAL = 'normal'
    HARD = 'hard'
    CHALLENGE = 'challenge'

class GeneratorType(enum.Enum):
    GENERAL = 'general'
    WORD = 'word'
    WORD_PAIRING = 'word-pairing'

class Question(Base):
    __tablename__ = 'questions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lessons.id'), nullable=False)
    difficulty = Column(Enum(Difficulty, name='difficulty'),  nullable=False, default=Difficulty.EASY)
    template = Column(JSONB)
    times_encountered = Column(Integer)
    times_correct = Column(Integer)
    generator_group_id = Column(UUID(as_uuid=True), ForeignKey('question_generator_groups.id'))

    __table_args__ = (
        # To get per-lesson history and user general history easily
        Index("idx_lesson_difficulty", "lesson_id", "difficulty"),
        UniqueConstraint("id", "lesson_id"),
    )

class QuestionHistory(Base):
    __tablename__ = 'question_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey('questions.id'), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lessons.id'), nullable=False)
    question_terms = Column(JSONB)
    question_answer = Column(JSONB)
    user_answer = Column(JSONB)
    correct = Column(Boolean, nullable=False)

    __table_args__ = (
        # To get per-lesson history and user general history easily
        Index("idx_history_user_lesson", "user_id", "lesson_id"),

        # so that we can query by lesson without it being expensive
        ForeignKeyConstraint(
            ["question_id", "lesson_id"],
            ["questions.id", "questions.lesson_id"]
        ),
    )

# There is going to be a group like WORD group corresponding to random words. PAIR word group corresponding to 
class QuestionGeneratorGroups(Base):
    __tablename__ = "question_generator_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generator_type = Column(Enum(GeneratorType, name='generator-type'), nullable=False)
    name = Column(String)

class QuestionPredefinedValues(Base):
    __tablename__ = "question_predefined_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generator_group_id = Column(UUID(as_uuid=True), ForeignKey('question_generator_groups.id'), nullable=False)
    value = Column(String)
    value_type = Column(String)
    pair_index = Column(Integer)
    # only valid if pair index
    pair_order = Column(Integer)

    __table_args__ = (
        Index("idx_generator_group_pair_index", "generator_group_id", "pair_index"),
    )