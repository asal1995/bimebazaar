import json

from fastapi import Response, status
from starlette.responses import JSONResponse


class CustomValidationError(Exception):
    pass


class ErrorJSONType(type):
    def __getattr__(self, item):
        error_code = getattr(ErrorCode, item)
        return {
            'code': error_code[0],
            'message': error_code[1]
        }


class ErrorCode:
    UNEXPECTED_ERROR = (1040010000, 'unexpected error')

    class dict(metaclass=ErrorJSONType):
        pass


def count(obj):
    if isinstance(obj, list):
        return len(obj)
    elif isinstance(obj, str) or isinstance(obj, dict) or isinstance(obj, int) or isinstance(obj, bool):
        return 1
    elif obj is None:
        return 0
    else:
        raise ValueError("Can not count items of %s" % type(obj))


def ok(data=None, result_number=None, reason=None):
    if reason:
        return JSONResponse((dict(message=data or reason[1], error=True, number=reason[0])))
    if not result_number:
        try:
            result_number = count(data)
        except Exception:
            result_number = len(data.items)

        try:  # used for pagination APIs
            data = data.dict()
        except Exception:
            pass
    return JSONResponse((dict(message=data, number=result_number, error=False)), status_code=status.HTTP_200_OK)


def created(data=None, result_number=None, reason=None):
    if reason:
        return Response(json.dumps(dict(message=data or reason[1], error=True, number=reason[0])))
    if not result_number:
        try:
            result_number = count(data)
        except Exception:
            result_number = len(data.items)

        try:  # used for pagination APIs
            data = data.dict()
        except Exception:
            pass
    return Response(
        json.dumps(dict(message=data, number=result_number, error=False), indent=4, sort_keys=True, default=str),
        status_code=status.HTTP_201_CREATED)


def bad_request(reason, message=None):
    return JSONResponse((dict(message=message or reason[1], error=True, number=reason[0])),
                        status_code=status.HTTP_400_BAD_REQUEST)


def internal_server_error(reason, message=None):
    return JSONResponse((dict(message=message or reason[1], error=True, number=reason[0])),
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def not_found(reason, message=None):
    return JSONResponse((dict(message=message or reason[1], error=True, number=reason[0])),
                        status_code=status.HTTP_404_NOT_FOUND)


class CustomException(Exception):

    def __init__(self, message):
        super().__init__(message)

    def http_response(self):
        raise NotImplementedError


class BadRequest(CustomException):

    def __init__(self, error_code: tuple):
        self.message = error_code
        super().__init__(self.message)

    def http_response(self):
        return bad_request(self.message)


class InternalServerError(CustomException):

    def __init__(self, error_code: tuple):
        self.message = error_code
        super().__init__(self.message)

    def http_response(self):
        return internal_server_error(self.message)


class NotFound(CustomException):

    def __init__(self, error_code: tuple):
        self.message = error_code
        super().__init__(self.message)

    def http_response(self):
        return not_found(self.message)
