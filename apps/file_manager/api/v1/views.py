from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileUploadSerializer
from apps.file_manager.services import handle_file_upload, determine_destination
from apps.file_manager.models import Files
from pprint import pprint
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils import timezone

class FileManager(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


    def post(self, request):
        parsed_data = {
            "attachments": request.FILES.getlist("attachments[]"),
            "type": request.data.get("type"),
        }
        
        serializer = FileUploadSerializer(data=parsed_data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data
        type = validated.get("type")
        attachments = validated.get("attachments")

        destination = determine_destination(type)
        if destination is None:
            raise ValidationError({ "file": [_("Upload type does not hava destination.")]})

        temp_files_destination = []
        for attachment in attachments:
            temp_file_path = handle_file_upload(attachment, destination)
            if temp_file_path is not None:
                temp_files_destination.append(temp_file_path)
               

        return Response(data={
            "files": temp_files_destination
        }, status=status.HTTP_200_OK)
