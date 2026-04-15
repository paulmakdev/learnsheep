from app.models.user import User
from app.models.lesson import Lesson
from app.core.security import hash_password
from app.models.question import Question, Difficulty, QuestionStyle
import logging
import pytest
import json


@pytest.fixture
def create_and_get_question(client, db):
    # seed the db directly
    user = User(
        email="test@test.com",
        hashed_salted_password=hash_password("password"),
        display_name="Test User",
    )
    lesson = Lesson(title="My Lesson", s3_key="some/key", lesson_metadata={})
    db.add(lesson)
    db.commit()
    db.add_all([user, lesson])
    db.commit()
    db.refresh(lesson)
    db.refresh(user)

    test_difficulty = Difficulty.EASY.value

    question = Question(
        lesson_id=lesson.id,
        difficulty=test_difficulty,
        template={
            "procedural_generators": {
                "addition_to_sum": {
                    "numbers": [
                        {
                            "config": {
                                "type": "int",
                                "min": 4,
                                "max": 10,
                            },
                            "name": "x_1",
                        },
                        {
                            "config": {
                                "type": "float",
                                "min": -5,
                                "max": 10,
                                "precision": 0,
                            },
                            "name": "x_2",
                        },
                        {
                            "config": {
                                "type": "int",
                                "min": -3,
                                "max": 3,
                            },
                            "name": "random_x_1",
                        },
                        {
                            "config": {
                                "type": "int",
                                "min": -3,
                                "max": 3,
                            },
                            "name": "random_x_2",
                        },
                    ],
                    "sum_name": "x_3",
                }
            },
            "choice_type": "numbers",
            "choices": ["x_3", "x_3-random_x_1", "x_1-x_2", "x_3+random_x_2"],
            "answers": ["x_3"],
            "question_expression": "x_1 + x_2 = ?",
            "question_type": "numbers",
        },
        question_style=QuestionStyle.MULTIPLE_CHOICE,
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    # get user token
    response = client.post(
        "/api/auth/login",
        json={"email": "test@test.com", "password": "password"},
    )
    response_json = response.json()
    token = response_json["access_token"]

    # hit the endpoint
    response = client.get(
        "/api/question/ask?lesson_id="
        + str(lesson.id)
        + "&difficulty="
        + str(test_difficulty),
        headers={"Authorization": f"Bearer {token}"},
    )
    return {"response": response, "access_token": token}


@pytest.fixture
def create_and_get_question_2(client, db):
    # seed the db directly
    user = User(
        email="test@test.com",
        hashed_salted_password=hash_password("password"),
        display_name="Test User",
    )
    lesson = Lesson(title="My Lesson", s3_key="some/key", lesson_metadata={})
    db.add(lesson)
    db.commit()
    db.add_all([user, lesson])
    db.commit()
    db.refresh(lesson)
    db.refresh(user)

    test_difficulty = Difficulty.EASY.value

    question = Question(
        lesson_id=lesson.id,
        difficulty=test_difficulty,
        template={
            "procedural_generators": {
                "addition_to_sum": {
                    "numbers": [
                        {
                            "config": {
                                "type": "int",
                                "min": 4,
                                "max": 10,
                            },
                            "name": "x_1",
                        },
                        {
                            "config": {
                                "type": "float",
                                "min": -5,
                                "max": 10,
                                "precision": 0,
                            },
                            "name": "x_2",
                        },
                        {
                            "config": {
                                "type": "int",
                                "min": -5,
                                "max": -1,
                            },
                            "name": "difference_maker_x_1",
                        },
                        {
                            "config": {
                                "type": "int",
                                "min": 1,
                                "max": 5,
                            },
                            "name": "difference_maker_x_2",
                        },
                    ],
                    "sum_name": "x_3",
                }
            },
            "choice_type": "numbers",
            "choices": [
                "x_3",
                "x_3-difference_maker_x_1",
                "x_1-x_2",
                "x_3+difference_maker_x_2",
            ],
            "answers": ["x_3"],
            "question_expression": "x_1 + x_2 = ?",
            "question_type": "numbers",
        },
        question_style=QuestionStyle.MULTIPLE_CHOICE,
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    # get user token
    response = client.post(
        "/api/auth/login",
        json={"email": "test@test.com", "password": "password"},
    )
    response_json = response.json()
    token = response_json["access_token"]

    # hit the endpoint
    response = client.get(
        "/api/question/ask?lesson_id="
        + str(lesson.id)
        + "&difficulty="
        + str(test_difficulty),
        headers={"Authorization": f"Bearer {token}"},
    )
    return {"response": response, "access_token": token}


def test_get_question(create_and_get_question):
    response = create_and_get_question["response"]
    assert response.status_code == 200


def test_answer_question_correct(create_and_get_question, client, db, cache):
    got_question = create_and_get_question["response"].json()
    token = create_and_get_question["access_token"]
    session_token = got_question["session_token"]
    current_user_id = db.query(User.id).filter(User.email == "test@test.com").scalar()
    stored_question = cache.get(session_token + ":" + str(current_user_id))
    stored_question_json = json.loads(stored_question)
    if stored_question is None:
        print("oh no")
    correct_answers = stored_question_json["answer_dict"]["answers"]
    answer = correct_answers[0]
    response = client.post(
        "/api/question/answer",
        json={"answer": answer, "session_token": session_token},
        headers={"Authorization": f"Bearer {token}"},
    )
    logger = logging.getLogger(__name__)

    logger.warning(response.json())
    assert response.json()["correct"]


def test_answer_question_incorrect(create_and_get_question_2, client, db, cache):
    got_question = create_and_get_question_2["response"].json()
    token = create_and_get_question_2["access_token"]
    session_token = got_question["session_token"]
    current_user_id = db.query(User.id).filter(User.email == "test@test.com").scalar()
    stored_question = cache.get(session_token + ":" + str(current_user_id))
    stored_question_json = json.loads(stored_question)
    if stored_question is None:
        print("oh no")
    choices = stored_question_json["answer_dict"]["choices"]
    answer = choices[0]
    if answer in stored_question_json["answer_dict"]["answers"]:
        answer = choices[1]
    response = client.post(
        "/api/question/answer",
        json={"answer": answer, "session_token": session_token},
        headers={"Authorization": f"Bearer {token}"},
    )
    logger = logging.getLogger(__name__)

    logger.warning(response.json())
    assert not response.json()["correct"]
