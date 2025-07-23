import time
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store timestamps of requests by IP: { ip_address: [timestamps] }
        self.ip_request_log = {}

    def __call__(self, request):
        # We only care about POST requests to message endpoints
        if request.method == "POST" and request.path.startswith("/api/messages/"):
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  # 1 minute in seconds
            max_requests = 5

            timestamps = self.ip_request_log.get(ip, [])

            # Remove timestamps older than the window
            timestamps = [ts for ts in timestamps if now - ts < window]

            if len(timestamps) >= max_requests:
                return JsonResponse(
                    {"detail": "Message limit exceeded. Please wait before sending more."},
                    status=429
                )

            timestamps.append(now)
            self.ip_request_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        """Helper to get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

