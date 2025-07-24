MIDDLEWARE = [
    # other default middlewares...
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
import time
from datetime import datetime
from django.http import HttpResponseForbidden

# Restrict chat access based on time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if not (18 <= current_hour <= 21):
            return HttpResponseForbidden("Access to chat is only allowed between 6PM and 9PM.")
        return self.get_response(request)


# ✅ NEW: Limit number of messages per IP address per minute
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = {}

    def __call__(self, request):
        # Only apply for POST requests (i.e., messages sent)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Initialize IP log if not already present
            if ip not in self.ip_message_log:
                self.ip_message_log[ip] = []

            # Remove entries older than 60 seconds
            self.ip_message_log[ip] = [
                timestamp for timestamp in self.ip_message_log[ip]
                if current_time - timestamp < 60
            ]

            # Check limit
            if len(self.ip_message_log[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute.")

            # Log this message
            self.ip_message_log[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
]

