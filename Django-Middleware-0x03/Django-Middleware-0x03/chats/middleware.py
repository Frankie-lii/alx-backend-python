import datetime
import json
from django.http import JsonResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method
        path = request.get_full_path()
        now = datetime.datetime.now().isoformat()

        log_entry = f"[{now}] {method} request made to {path}\n"

        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.datetime.now()
        if now.hour < 8 or now.hour >= 17:
            return JsonResponse({"error": "Access restricted to business hours (8AM - 5PM)"}, status=403)

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.offensive_words = ['badword1', 'badword2', 'offensive']  # Replace with real offensive words

    def __call__(self, request):
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.body:
                try:
                    data = json.loads(request.body.decode('utf-8'))
                    for key, value in data.items():
                        if isinstance(value, str):
                            for word in self.offensive_words:
                                if word.lower() in value.lower():
                                    return JsonResponse({"error": "Offensive language detected"}, status=400)
                except json.JSONDecodeError:
                    pass

        return self.get_response(request)


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if request.path.startswith('/admin/') or request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            if not user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=403)
            if not (user.is_staff or user.is_superuser):
                return JsonResponse({'error': 'Permission denied. Only admins or moderators allowed.'}, status=403)

        return self.get_response(request)

