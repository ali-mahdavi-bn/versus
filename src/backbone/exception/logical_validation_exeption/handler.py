from starlette.requests import Request
from starlette.responses import JSONResponse

from backbone.api.translator.translator import translate
from backbone.exception.logical_validation_exeption.exeptions import LogicalValidationException


def logical_validation_handler(request: Request, exception: LogicalValidationException) -> JSONResponse:

    return JSONResponse({'message': "Inputted data was invalid.", 'errors': [{
        "loc": exception.loc,
        "message": translate(exception.message, **exception.payload),
        "type": exception.type
    }]}, status_code=422)
