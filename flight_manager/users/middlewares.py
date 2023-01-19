import json

from django.utils.deprecation import MiddlewareMixin


class JSONParsingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if (
            request.method == "PUT"
            or request.method == "POST"
            or request.method == "PATCH"
        ) and request.content_type == "application/json":
            try:
                request.JSON = json.loads(request.body)
            except None as n:
                return n
