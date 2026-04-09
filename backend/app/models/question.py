from sqlalchemy import (
    Column,
    String,
    Enum,
    Boolean,
    ForeignKey,
    Index,
    ForeignKeyConstraint,
    Integer,
    UniqueConstraint,
)
import enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.core.database import Base


class OrderedEnum(enum.Enum):
    def __lt__(self, other):
        members = list(self.__class__)
        return members.index(self) < members.index(other)

    def __gt__(self, other):
        members = list(self.__class__)
        return members.index(self) > members.index(other)


class Difficulty(str, OrderedEnum):
    # order matters here for downgrading difficulty
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    CHALLENGE = "challenge"

    # get easier difficulty, or get None if already easy
    def downgrade(self):
        members = list(Difficulty)
        current_index = members.index(self)
        if current_index == 0:
            return None
        return members[current_index - 1]

    # get harder difficulty, or get None if already challenge
    def upgrade(self):
        members = list(Difficulty)
        current_index = members.index(self)
        if current_index == 3:
            return None
        return members[current_index + 1]


class QuestionStyle(str, enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TEXTBOX = "textbox"


class GeneratorType(str, enum.Enum):
    GENERAL = "general"
    WORD = "word"
    WORD_PAIRING = "word-pairing"


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    difficulty = Column(
        Enum(Difficulty, name="difficulty"), nullable=False, default=Difficulty.EASY
    )
    template = Column(JSONB)
    question_style = Column(
        Enum(QuestionStyle, name="question_style"),
        nullable=False,
        default=QuestionStyle.TEXTBOX,
    )
    times_encountered = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)
    generator_group_id = Column(
        UUID(as_uuid=True), ForeignKey("question_generator_groups.id")
    )

    __table_args__ = (
        # To get per-lesson history and user general history easily
        Index("idx_lesson_difficulty", "lesson_id", "difficulty"),
        UniqueConstraint("id", "lesson_id"),
    )


class QuestionHistory(Base):
    __tablename__ = "question_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    question_values = Column(JSONB)
    question_choices = Column(JSONB)
    question_answers = Column(JSONB)
    user_answer = Column(JSONB)
    correct = Column(Boolean, nullable=False)

    __table_args__ = (
        # To get per-lesson history and user general history easily
        Index("idx_history_user_lesson", "user_id", "lesson_id"),
        # so that we can query by lesson without it being expensive
        ForeignKeyConstraint(
            ["question_id", "lesson_id"], ["questions.id", "questions.lesson_id"]
        ),
    )


# There is going to be a group like WORD group corresponding to random words. PAIR word group corresponding to
class QuestionGeneratorGroups(Base):
    __tablename__ = "question_generator_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generator_type = Column(Enum(GeneratorType, name="generator-type"), nullable=False)
    name = Column(String)


class QuestionPredefinedValues(Base):
    __tablename__ = "question_predefined_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generator_group_id = Column(
        UUID(as_uuid=True), ForeignKey("question_generator_groups.id"), nullable=False
    )
    value = Column(String)
    value_type = Column(String)
    pair_index = Column(Integer)
    # only valid if pair index
    pair_order = Column(Integer)

    __table_args__ = (
        Index("idx_generator_group_pair_index", "generator_group_id", "pair_index"),
    )
