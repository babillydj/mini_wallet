from rest_framework.renderers import JSONRenderer
from rest_framework import status as drf_status
from rest_framework.response import Response


class BaseResponse(Response):
    def __init__(self, data=None, message=None, status=drf_status.HTTP_200_OK):
        response = {
            "status": "success" if drf_status.is_success(status) else "failed",
            "data": data,
        }

        if message:
            response["message"] = message

        super(BaseResponse, self).__init__(response, status=status)
