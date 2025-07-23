from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 6PM (18) and 9PM (21)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Chat access is only allowed between 6PM and 9PM.")
        return self.get_response(request)

