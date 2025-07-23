from django.db import models

# Create your models here.
class Files(models.Model):
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(
        max_length=255,
    )
    file_size = models.FloatField()
    mime_type = models.CharField(
        max_length=50
    )
    model = models.CharField(
        max_length=100,
        null=False
    )
    model_id = models.BigIntegerField()
    deleted_at = models.DateTimeField(
        null=True
    )
