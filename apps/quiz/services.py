from django.db import transaction
from pprint import pprint
from common.mixins.file_mixins import ExtractContent
from apps.quiz.models import Quizzes, Questions, Answers
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from django.utils import timezone

class QuizSvc:
   
    @staticmethod
    def generate_quiz(**kwargs):
        questions = kwargs.get("json_data")["questions"]
        with transaction.atomic():
            quiz = QuizSvc.create_questions(
                created_at=timezone.now(),
                title=kwargs.get("title"),
                description=kwargs.get("description"),
                type=kwargs.get("type"),
            )
            for question in questions:
                new_question = QuizSvc.add_question(
                    quiz,
                    created_at=timezone.now(),
                    question=question["question"],
                    type=question["type"],
                    difficulty=question["difficulty"],
                )
                for answer in question["answers"]:
                    QuizSvc.add_answer(
                        new_question,
                        created_at=timezone.now(),
                        answer=answer["answer"],
                        is_correct=bool(answer["is_correct"]),
                    )
            return quiz


    @staticmethod
    def create_questions(**kwargs):
        return Quizzes.objects.create(
            created_at=kwargs.get("created_at"),
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            type=kwargs.get("type"),
            is_active=True
        )

    @staticmethod
    def add_question(quiz, **kwargs):
        return Questions.objects.create(
            created_at=kwargs.get("created_at"),
            question=kwargs.get("question"),
            type=kwargs.get("type"),
            difficulty=kwargs.get("difficulty"),
            quiz=quiz
        )

    @staticmethod
    def add_answer(question, **kwargs):
        return Answers.objects.create(
            created_at=kwargs.get("created_at"),
            answer=kwargs.get("answer"),
            is_correct=bool(kwargs.get("is_correct")),
            question=question
        )
    
class OpenAISvc:
   
    def __init__(self):
        self.client = OpenAI()

    def query(self, **kwargs):
        input = kwargs.get("input", "")

        if input == "":
            return False

        response = self.client.responses.create(
            model="gpt-4.1-nano-2025-04-14",
            input= input
        )
        return response.output_text
