from typing import List, Dict

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


def validation_exception_handler(request: Request, exception: RequestValidationError):
    errors: List[Dict] = exception.errors()
    structure_errors = []
    for error in errors:
        location = ".".join([str(location) for location in error['loc']])
        type_ = error['type']
        message: str = 'pydantic.' + str(error['type'])
        structure_errors.append({'location': location, 'type': type_, 'message': message})
    return JSONResponse({'message': "Inputted data was invalid", 'errors': structure_errors}, status_code=422)
