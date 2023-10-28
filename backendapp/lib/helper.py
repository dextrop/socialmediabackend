from rest_framework.exceptions import ValidationError

def validate_request(data, keys):
    resp = dict()
    for key in keys:
        val = data.get(key, None)
        if not val:
            raise ValidationError(f"Missing {key} in request")
        resp[key] = val
    return True
