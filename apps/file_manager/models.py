from django.db import models
import uuid

# Create your models here.
class Files(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(
        max_length=255,
    )
    size = models.FloatField()
    mime_type = models.CharField(
        max_length=150
    )
    model = models.CharField(
        max_length=100,
        null=True
    )
    model_id = models.BigIntegerField(
        null=True
    )
    deleted_at = models.DateTimeField(
        null=True
    )
