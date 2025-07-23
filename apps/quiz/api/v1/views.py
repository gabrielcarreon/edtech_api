from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from apps.quiz.models import Quizzes
from .serializers import QuizzesSerializer, AIGenerationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions, status
from pprint import pprint
from pathlib import Path
from apps.quiz.services import OpenAISvc
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

class QuizzesListCreate(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request, format=None):
        queryset = Quizzes.objects.all().order_by("title")
        serializer = QuizzesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        data = request.data.copy()
        files = request.FILES.getlist("attachments[]")
        data.setlist("attachments", files)

        quiz_data_serializer = QuizzesSerializer(data=data)
        quiz_data_serializer.is_valid(raise_exception=True)
    
        quiz_data = quiz_data_serializer.validated_data
        type = quiz_data.get("type")

        if type == "ai":
            if files is None:
                raise ValidationError({ "attachments": [_("Must have at least 1 (one) file to continue.")] })
            
            generation_data_serializer = AIGenerationSerializer(data=data)
            generation_data_serializer.is_valid(raise_exception=True)
            generation_data = generation_data_serializer.validated_data

            files = generation_data.get("attachments")
            question_type = generation_data.get("question_type")
            difficulty = generation_data.get("difficulty")
            focus_area = generation_data.get("focus_area")

            p = Path(__file__).resolve().parent.parent / "open_ai" / "quiz_generation_prompt.txt"
            with p.open("r") as f:
                prompt = f.read()
                f.close()

            # extracted_texts = []
            # for file in files:
            #     extracted_texts.append(ExtractContent.extract_document(file))

            # svc = OpenAISvc()
            # raw = svc.query(input="\n".join(extracted_texts))
            # Now generate the quiz based on the following text:
            # cleaned = raw.strip("`").replace("```json", "").replace("```", "").strip()
            # parsed = json.loads(cleaned)

            # QuizSvc.generate_quiz(
            #     title=validated.get("title"),
            #     description=validated.get("description"),
            #     type=validated.get("type"),
            #     json_data=parsed
            # )
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
        