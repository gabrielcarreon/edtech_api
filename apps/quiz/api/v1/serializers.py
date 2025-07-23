from rest_framework import serializers
from apps.quiz.models import Quizzes
from pprint import pprint
from dotenv import load_dotenv
from common.mixins.file_mixins import FileValidationMixin

load_dotenv()

class QuizzesSerializer(serializers.ModelSerializer):
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
    

    class Meta:
        model = Quizzes
        fields = [
            "id",
            "title", 
            "type",
            "description",
        ]

class QuestionTypeSerializer(serializers.Serializer):
    true_or_false=serializers.IntegerField(
        required=True,
    )
    essay_question=serializers.IntegerField(
        required=True,
    )

class AIGenerationSerializer(serializers.Serializer, FileValidationMixin):
    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        allow_empty=True
    )
    difficulty = serializers.ChoiceField(
        choices=["easy", "moderate", "hard", "mixed"],
        required=True,
        allow_blank=False,
    )
    focus_area = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )
    question_type = QuestionTypeSerializer()


    def validate_question_type(self, value):
        pprint(value)
        # if not any(val > 0 for val in value.values()):
        #     raise serializers.ValidationError("At least one question type must be greater than zero.")
        return value

    def validate_attachments(self, files):
        for file in files:
            self.validate_file(file)
        return files