from app.models.user import User
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.core.security import hash_password


def test_create_progress_and_get(client, db):
    user_email = "test@test.com"
    user_password = "password"
    lesson_title = "My Lesson"
    lesson_slug = "some/key"
    progress_level = 69

    # seed the db directly
    user = User(
        email=user_email,
        hashed_salted_password=hash_password(user_password),
        display_name="Test User",
    )
    lesson = Lesson(title=lesson_title, s3_key=lesson_slug, lesson_metadata={})

    db.add(lesson)
    db.commit()
    db.add_all([user, lesson])
    db.commit()
    db.refresh(lesson)
    db.refresh(user)
    current_user_id = db.query(User.id).filter(User.email == user_email).scalar()
    lesson_id = db.query(Lesson.id).filter(Lesson.title == lesson_title).scalar()
    progress = Progress(
        user_id=current_user_id, lesson_id=lesson_id, level=progress_level, level_xp=0
    )
    db.add(progress)
    db.commit()
    db.refresh(progress)

    # get user token
    login_response = client.post(
        "/api/auth/login",
        json={"email": user_email, "password": user_password},
    )
    login_response_json = login_response.json()
    access_token = login_response_json["access_token"]

    progress_response = client.get(
        "/api/stat/progress",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert progress_response.status_code == 200
