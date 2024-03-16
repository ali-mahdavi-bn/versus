from starlette.requests import Request
from starlette.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

