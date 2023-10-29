import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

VALIDATION = {
    "/comment/": {
        "POST": ["post_id", "comment"],
    }
}

class RequestValidator(MiddlewareMixin):
    """Middleware for Request Validation"""
    def validate_request(self, data, keys, request):
        for key in keys:
            if key not in data:
                return JsonResponse({
                    'code': 400,
                    'message': f"missing {key} in request data"
                }, status=400)

        return self.get_response(request)


    def process_request(self, request):
        if request.path in VALIDATION and request.method in VALIDATION[request.path]:
            try:
                json_data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError as e:
                print (e)
                return self.get_response(request)

            return self.validate_request(
                json_data, VALIDATION[request.path][request.method], request
            )
        return self.get_response(request)
