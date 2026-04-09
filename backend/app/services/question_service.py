import random
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.question import (
    Question,
    QuestionHistory,
    Difficulty,
    QuestionPredefinedValues,
)
from app.models.progress import Progress
from app.models.user import User
from app.schemas.question import (
    QuestionRequest,
    AnswerRequest,
    QuestionResponse,
    AnswerResponse,
)
from app.core.cache import CacheService
from app.core.exceptions import NoQuestionsFoundError
from sympy import sympify, nsimplify
import secrets
import json
import re
from app.core.levelup import handle_xp_change


def get_question(
    db: Session,
    cache: CacheService,
    current_user: User,
    question_request: QuestionRequest,
) -> QuestionResponse:
    """Chooses a question, generates values, replaces variables, and returns relevant information for user."""

    question = choose_question(db, question_request)
    variable_replacement_dict = get_variable_values(db, question)
    answer_dict = get_choices_answers_variables_replaced(
        question, variable_replacement_dict
    )
    print(question)
    question_expression = get_question_expression_variables_replaced(
        question, variable_replacement_dict
    )
    choices = answer_dict["choices"]
    del question.template["answers"]

    # We use a session token for the cached answer so they can't tell which question id we are sending, helps prevent cheating
    session_token = secrets.token_hex(32)
    cache.set(
        session_token + ":" + str(current_user.id),
        json.dumps(
            {
                "answer_dict": answer_dict,
                "values": variable_replacement_dict,
                "question_id": str(question.id),
                "lesson_id": str(question.lesson_id),
                "user_id": str(current_user.id),
            }
        ),
        ttl=1800,
    )

    return {
        "question_expression": question_expression,
        "question_template": question.template,
        "values": variable_replacement_dict,
        "choices": choices,
        "session_token": session_token,
    }


def choose_question(db: Session, question_request: QuestionRequest) -> Question:
    """Chooses a lesson question based on difficulty, if no questions for lesson throws NoQuestionsFoundError."""

    current_difficulty = question_request.difficulty
    while current_difficulty is not None:
        questions = db.query(Question).filter(
            Question.lesson_id == question_request.lesson_id
            and Question.difficulty == question_request.difficulty
        )
        if questions:
            return questions.order_by(func.random()).first()

        current_difficulty = current_difficulty.downgrade()

    current_difficulty = question_request.upgrade()

    while current_difficulty is not None:
        questions = db.query(Question).filter(
            Question.lesson_id == question_request.lesson_id
            and Question.difficulty == question_request.difficulty
        )
        if questions:
            return questions.order_by(func.random()).first()

        current_difficulty = current_difficulty.upgrade()

    raise NoQuestionsFoundError


def get_variable_values(db: Session, question: Question) -> dict:
    """Returns a dictionary that contains variables as the keys and values as the values for the question."""
    value_dict = {}

    if "procedural_generators" in question.template:
        value_dict = function_generator_mapper(
            question.template["procedural_generators"]
        )

    if question.generator_group_id is None:
        return value_dict

    values = db.query(QuestionPredefinedValues).filter(
        QuestionPredefinedValues.generator_group_id == question.generator_group_id
    )
    if values:
        values = values.all()
        value_dict = {}
        for value in values:
            value_dict[value.value_type] = value.value

    return value_dict


def function_generator_mapper(generators: dict) -> dict:
    """Goes through all necessary function generators necessary and generates values as described."""
    result_dict = {}
    for key in generators.keys():
        function = function_generators.get(key)
        if function:
            result_dict = result_dict | function(generators[key])

    return result_dict


def addition_to_sum(generator_config: dict) -> dict:
    """Generates various numbers and returns the sum.

    Sample generator_config:
                {
                    "numbers":
                        [
                            {
                                "config": {
                                    "type": "int",
                                    "min": -3,
                                    "max": 3,
                                },
                                "name": "random_x_1"
                            },
                            {
                                "config": {
                                    "type": "int",
                                    "min": -3,
                                    "max": 3,
                                },
                                "name": "random_x_2"
                            }
                    ],
                    "sum_name": "random_x_3",
                }
    """
    result_dict = {}
    total_sum = 0
    for number_metadata in generator_config["numbers"]:
        number_config = number_metadata["config"]
        number_name = number_metadata["name"]
        returned_number = random_number_generator(
            NumberGeneratorConfig(**number_config)
        )
        if "difference_maker_" not in number_name:
            total_sum += returned_number
        result_dict[number_name] = returned_number

    sum_name = generator_config["sum_name"]
    result_dict[sum_name] = total_sum
    return result_dict


class NumberGeneratorConfig(BaseModel):
    """Used for generating numbers, either ints or floats"""

    type: str
    min: int | float
    max: int | float
    precision: int = 0  # decimal places for floats


def random_number_generator(config: NumberGeneratorConfig) -> int | float:
    """Function that generates numbers based on config."""
    if config.type == "int":
        return random.randint(int(config.min), int(config.max))
    elif config.type == "float":
        return round(random.uniform(config.min, config.max), config.precision)


def get_choices_answers_variables_replaced(question: Question, values: dict) -> dict:
    """Replaces unknown variables with variable values in answers and answer choices."""

    template = question.template
    choices = []
    answers = []
    if "hardcoded" in template["choice_type"]:
        choices = template["choices"]
        answers = template["answers"]
        return {"choices": choices, "answers": answers}

    list_values = list(values.items())

    if "numbers" in template["choice_type"]:
        choices = template["choices"]
        replaced_choices = []
        for choice in choices:
            choice = sympify(choice)
            choice = choice.subs(list_values)
            choice = nsimplify(choice)
            replaced_choices.append(str(choice))

        answers = template["answers"]
        replaced_answers = []
        for answer in answers:
            answer = sympify(answer)
            answer = answer.subs(list_values)
            answer = nsimplify(answer)
            replaced_answers.append(str(answer))
        return {"answers": replaced_answers, "choices": replaced_choices}

    return {"answers": answers, "choices": choices}


def get_question_expression_variables_replaced(
    question: Question, variable_replacement_dict: dict
) -> str:
    """Replaces unknown variables in question expression."""
    template = question.template
    question_expression = template["question_expression"]

    if "hardcoded" in template["question_type"]:
        return question_expression

    if "numbers" in template["question_type"]:
        for variable, value in variable_replacement_dict.items():
            question_expression = re.sub(
                rf"\b{re.escape(str(variable))}\b", str(value), question_expression
            )
        print(question_expression)
        return question_expression

    return ""


# Defines how much xp to get from each question difficulty
xp_from_difficulty = {
    Difficulty.EASY: 1,
    Difficulty.NORMAL: 2,
    Difficulty.HARD: 4,
    Difficulty.CHALLENGE: 8,
}


def answer_question(
    db: Session, cache: CacheService, current_user: User, answer_request: AnswerRequest
) -> AnswerResponse:
    """Checks if answer is correct, records question and answer in QuestionHistory, and updates Progress with xp / level."""

    cached_info = json.loads(
        cache.get(answer_request.session_token + ":" + str(current_user.id))
    )

    if cached_info:
        correct_bool = answer_request.answer in cached_info.get("answer_dict", {}).get(
            "answers", []
        )
        history = QuestionHistory(
            user_id=current_user.id,
            question_id=cached_info["question_id"],
            lesson_id=cached_info["lesson_id"],
            question_values=cached_info.get("values", []),
            question_choices=cached_info.get("answer_dict", {}).get("choices", []),
            question_answers=cached_info.get("answer_dict", {}).get("answers", []),
            user_answer=answer_request.answer,
            correct=correct_bool,
        )
        db.add(history)
        db.commit()
        cache.delete(
            cache.get(answer_request.session_token + ":" + str(current_user.id))
        )

        question = db.get(Question, cached_info["question_id"])
        question.times_encountered += 1
        question.times_correct += 1 if correct_bool else 0

        progress = (
            db.query(Progress)
            .filter(
                Progress.user_id == current_user.id,
                Progress.lesson_id == question.lesson_id,
            )
            .first()
        )
        xp_change = xp_from_difficulty.get(question.difficulty, 1) * (
            1 if correct_bool else -1
        )
        if progress is None:
            streak = 0
            current_level = 1
            level_xp = 0
            progress = Progress(
                user_id=current_user.id,
                lesson_id=question.lesson_id,
                level_xp=level_xp,
            )
            db.add(progress)
            db.commit()
            db.refresh(progress)
        else:
            streak = progress.streak
            current_level = progress.current_level
            level_xp = progress.level_xp

        result_change = handle_xp_change(
            level_xp=level_xp,
            current_level=current_level,
            xp_change=xp_change,
            streak=streak,
        )
        progress.current_level = result_change.get("current_level", 1)
        progress.level_xp = result_change.get("level_xp", 0)
        progress.streak += 1 if correct_bool else -progress.streak
        progress.answered_questions += 1
        progress.questions_correct += 1 if correct_bool else 0
        progress.questions_incorrect += 0 if correct_bool else 1
        db.commit()

        return {
            "correct": correct_bool,
            "new_xp": result_change.get("current_level", 1),
            "new_level": result_change.get("level_xp", 0),
        }
    else:
        raise ValueError("Invalid session token (expired) or wrong user.")


function_generators = {"addition_to_sum": addition_to_sum}
