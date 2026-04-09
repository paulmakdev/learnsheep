class NoQuestionsFoundError(Exception):
    def __init__(self, lesson_id, difficulty):
        self.lesson_id = lesson_id
        self.original_difficulty = difficulty
