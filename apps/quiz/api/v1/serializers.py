from rest_framework import serializers
from apps.quiz.models import Quiz, Question, Answer
from pprint import pprint
from dotenv import load_dotenv
from common.mixins.file_mixins import FileValidationMixin

load_dotenv()

class AnswerSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(
        max_length = 255,
        required = True,
        allow_blank = False,
    )
    is_correct = serializers.BooleanField()
    
    class Meta:
        model = Answer
        fields = [
            "answer",
            "is_correct",
        ]

class QuestionSerializer(serializers.ModelSerializer):
    question = serializers.CharField(
        max_length = 255,
        required = True,
        allow_blank = False,
    )
    type = serializers.ChoiceField(
        choices=["true_or_false", "fill_in_the_blank", "multiple_choice", "essay"],
    )
    difficulty = serializers.ChoiceField(
        choices=["easy", "medium", "hard"]
    )
    is_active = serializers.BooleanField()
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "quiz_id",
            "question",
            "type",
            "difficulty",
            "is_active",
            "answers"
        ]


class QuizSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True, 
        allow_blank=False,
        max_length=255,
        error_messages={
            "required": "Title is required",
            "blank": "Title is required",
            "max_length": "Title is too long",
        }
    )
    description = serializers.CharField(
        required=False, 
        allow_blank=True,
    )
    type = serializers.ChoiceField(
        required=True, 
        allow_blank=False,
        choices=["ai", "manual"],
        error_messages={
            "required": "Type is required",
            "blank": "Type is required",
            "choices": "Type must be either ai or manual",
        }
    )
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = [
            "id",
            "title", 
            "type",
            "description",
            "questions"
        ]


class AttachmentSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=255
    )
    timestamp = serializers.CharField(
        required=True,
    )
    uuid = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=255
    )

class QuestionTypeSerializer(serializers.Serializer):
    true_or_false=serializers.IntegerField(
        required=True,
    )
    essay_question=serializers.IntegerField(
        required=True,
    )
    fill_in_the_blank=serializers.IntegerField(
        required=True,
    )
    multiple_choice=serializers.IntegerField(
        required=True,
    )

class AIGenerationSerializer(serializers.Serializer, FileValidationMixin):
    attachments = serializers.ListField(
        child = AttachmentSerializer(),
        required = False,
        allow_empty = True
    )
    difficulty = serializers.ChoiceField(
        choices=["easy", "moderate", "hard", "mixed"],
        required=True,
        allow_blank=False,
    )
    focus_areas = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )
    question_type = QuestionTypeSerializer()