from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    is_success,
)

class CustomResponse(Response):
    def __init__(self,message=None, code=HTTP_200_OK, payload=None):

        data = {"status": True, "payload": payload, "message": message}

        if not is_success(code=code):
            data["status"] = False

            error_data = {
                "code": code,
            }
            if code == 401:
                code = HTTP_401_UNAUTHORIZED
            elif code == 403:
                code = HTTP_403_FORBIDDEN
            else:
                code = HTTP_400_BAD_REQUEST
            data["error"] = error_data

        super(CustomResponse, self).__init__(data=data, status=code)
