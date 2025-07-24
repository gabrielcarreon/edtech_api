from rest_framework import serializers
from common.mixins.file_mixins import FileValidationMixin
from pprint import pprint

class FileUploadSerializer(serializers.Serializer, FileValidationMixin):
    type = serializers.ChoiceField(
        choices=["avatar", "document"]
    )
    attachments = serializers.ListField(
        child = serializers.FileField(),
        required = True,
    )

    def validate_attachments(self, files):
        for file in files:
            self.validate_file(file)
        return files