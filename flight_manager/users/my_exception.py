from rest_framework import status
from rest_framework.exceptions import PermissionDenied


class MyCustomException(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Custom Exception Message"
    default_code = "invalid"

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)
#
#     if response is not None:
#         exc_list = str(exc).split("DETAIL")
#
#     return response
