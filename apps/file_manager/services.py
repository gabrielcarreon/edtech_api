import os
from pathlib import Path
from dotenv import load_dotenv
from pprint import pprint
import time
from apps.file_manager.models import Files
from django.utils import timezone

load_dotenv()

def handle_file_upload(file, destination):
    timestamp = str(time.time()).replace(".", "_")
    file_path = Path(os.getenv("PROJECT_PATH")) / destination / f"{timestamp}_{file.name}"
    
    try:
        with open(file_path, "xb") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        db_file = Files.objects.create(
                        created_at = timezone.now(),
                        file_name = file.name,
                        size = file.size,
                        mime_type = file.content_type
                    )
        return {
            "filename": file.name,
            "timestamp": timestamp,
            "uuid": db_file.uuid
        }
    except:
        return None


def determine_destination(type):
    match type:
        case "document":
            return "media/documents"
        case "avatar":
            return "media/avatars"
        case _:
            return None