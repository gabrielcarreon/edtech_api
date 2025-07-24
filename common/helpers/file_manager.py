from apps.file_manager.models import Files

def retrieve_file_metadata(uuid):
    return Files.objects.get(uuid=uuid)