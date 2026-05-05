from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.progress import Progress
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.stat import OutboundProgressResponse


def get_ordered_progress(db: Session, current_user: User) -> OutboundProgressResponse:
    """Gets all opened lessons and progress on that lesson, along with the lesson slug."""

    history_query = (
        select(
            Progress.level,
            Progress.level_xp,
            Progress.streak,
            Progress.answered_questions,
            Progress.questions_correct,
            Progress.questions_incorrect,
            Progress.updated_at,
            Progress.created_at,
            Lesson.s3_key.label("lesson_slug"),
        )
        .join(Progress, Progress.lesson_id == Lesson.id)
        .where(Progress.user_id == current_user.id)
        .order_by(Progress.updated_at.desc())
    )

    history = db.execute(history_query).mappings().all()

    return {"items": history}
