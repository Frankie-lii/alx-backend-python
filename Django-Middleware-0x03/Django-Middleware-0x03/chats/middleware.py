from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Only allow between 18:00 (6 PM) and 21:00 (9 PM) inclusive
        if not (18 <= current_hour <= 21):
            return HttpResponseForbidden("Access to chat is only allowed between 6PM and 9PM.")
        return self.get_response(request)

