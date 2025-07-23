from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.exceptions import ValidationError

def custom_validation_exception(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and response is not None:
        response.data = {
            "message": "The given data was invalid",
            "errors": response.data
        }
    return response
