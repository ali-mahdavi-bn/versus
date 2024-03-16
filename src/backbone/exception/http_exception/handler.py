from fastapi import HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from backbone.api.translator.translator import translate


def http_exception_handler(request: Request, exception: HTTPException) -> JSONResponse:
    if exception.status_code == status.HTTP_403_FORBIDDEN:
        resource = translate(exception.resource, dictionary_type='resource_access')
        scope = translate(exception.scope, dictionary_type='resource_access')
        exception.detail = translate(exception.detail, permission=f"{scope} {resource}") if resource else translate(
            exception.detail)
        return JSONResponse({"detail": exception.detail}, status_code=exception.status_code)

    body = {"detail": translate(exception.detail)}

    return JSONResponse(body, status_code=exception.status_code)
