from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import Response, exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    if response is not None:
        response.data = Response(
            {
                "success": False,
                "error": exc.args,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
        return response.data
    elif isinstance(exc, IntegrityError):
        response = Response(
            {"success": False, "error": str(exc).strip("\n").split("DETAIL:  ")[-1]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    elif isinstance(exc, ValueError) or isinstance(exc, ObjectDoesNotExist):
        response = Response(
            {"success": False, "error": {str(exc.__class__.__name__): str(exc)}},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif isinstance(exc, KeyError):
        response = Response(
            {"success": False, "error": "Invalid Parameters"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return response
