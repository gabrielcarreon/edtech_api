from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from apps.quiz.models import Quiz
from .serializers import QuizSerializer, AIGenerationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions, status
from pprint import pprint
from pathlib import Path
from apps.quiz.services import OpenAISvc
from dotenv import load_dotenv
from django.core.files import File
from pathlib import Path
from common.helpers.file_manager import retrieve_file_metadata
from common.mixins.file_mixins import ExtractContent
from jinja2 import Template
import os
from apps.quiz.services import QuizSvc
import json
from django.shortcuts import get_object_or_404

load_dotenv()

class QuizzesCreate(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser]
    
    def get(self, request, format=None):
        queryset = Quiz.objects.all().order_by("title")
        serializer = QuizSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        quiz_data_serializer = QuizSerializer(data=request.data)
        quiz_data_serializer.is_valid(raise_exception=True)
    
        quiz_data = quiz_data_serializer.validated_data
        type = quiz_data.get("type")
        files = quiz_data.get("attachments")


        if type == "ai":
            generation_data_serializer = AIGenerationSerializer(data=request.data)
            generation_data_serializer.is_valid(raise_exception=True)
            generation_data = generation_data_serializer.validated_data

            files = generation_data.get("attachments")

            if files is None:
                raise ValidationError({ "attachments": [_("Must have at least 1 (one) file to continue.")] })
            
            question_type = generation_data.get("question_type")
            difficulty = generation_data.get("difficulty")
            focus_areas = generation_data.get("focus_areas")

            quiz_config = {
                "difficulty": difficulty,
                "fill_in_the_blank": question_type["fill_in_the_blank"],
                "true_or_false": question_type["true_or_false"],
                "essay_question": question_type["essay_question"],
                "multiple_choice": question_type["multiple_choice"],
                "focus_areas": focus_areas
            }

            p = Path(os.getenv("PROJECT_PATH")) / "static" / "quiz_generation_prompt.txt"

            with open(p, "r") as f:
                template = Template(f.read())

            prompt = template.render(quiz_config)

            extracted_texts = []
            for file in files:
                timestamp = file["timestamp"]
                name = file["name"]
                file_path = Path(os.getenv("PROJECT_PATH")) / "media" / "documents" / f"{timestamp}_{name}"
                with open(file_path, "rb") as f:
                    disk_file = File(f)

                    file_meta_data = retrieve_file_metadata(uuid=file["uuid"])
                    extracted_texts.append(ExtractContent.extract_document(file_meta_data.mime_type, disk_file))

            svc = OpenAISvc()
            raw = svc.query(input=prompt+"\n".join(extracted_texts))
            cleaned = raw.strip("`").replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)

            # with open(Path(os.getenv("PROJECT_PATH")) / "static" / "response.json", "r") as f:
            #     parsed = json.load(f)

            QuizSvc.generate_quiz(
                title=quiz_data.get("title"),
                description=quiz_data.get("description"),
                type=quiz_data.get("type"),
                json_data=parsed
            )
            pass
        else:
            title = request.data.get("title")
            description = request.data.get("description")
            pass
        
        
        return Response(status=status.HTTP_200_OK)


        # quiz = Quizzes()
        # quiz.title = title
        # quiz.description = description
        # quiz.created_at = datetime.datetime.now()
        # quiz.save()

class QuizShow(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser]

    def get(self, request, id):
        quiz = get_object_or_404(Quiz, id=id)
        serializer = QuizSerializer(quiz, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)