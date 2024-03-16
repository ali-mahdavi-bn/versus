from fastapi import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, detail):
        super(BadRequestException, self).__init__(status_code=400)
        self.detail = detail


class UnauthorizedException(HTTPException):
    def __init__(self):
        super(UnauthorizedException, self).__init__(status_code=401)
        self.detail = "Unauthenticated"


class UnsupportedMediaTypeException(HTTPException):
    def __init__(self):
        super(UnsupportedMediaTypeException, self).__init__(status_code=415)


class ForbiddenException(HTTPException):
    def __init__(self, detail=None, resource=None, scope=None):
        super(ForbiddenException, self).__init__(status_code=403)
        self.detail = detail
        self.resource = resource
        self.scope = scope


class NotFoundException(HTTPException):
    def __init__(self, detail=None):
        super(NotFoundException, self).__init__(status_code=404)
        self.detail = detail


class HTTPNotImplemented(HTTPException):
    def __init__(self, detail=None):
        super(HTTPNotImplemented, self).__init__(status_code=501)
        self.detail = detail


class ConflictException(HTTPException):
    def __init__(self):
        super(ConflictException, self).__init__(status_code=409)


class InternalServerException(HTTPException):
    def __init__(self, detail):
        super(InternalServerException, self).__init__(status_code=500)
        self.detail = detail

    def __str__(self):
        return self.detail
