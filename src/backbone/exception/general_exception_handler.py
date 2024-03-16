from typing import List, Dict

import sentry_sdk
from starlette.requests import Request
from starlette.responses import JSONResponse

from backbone.api.translator.translator import translate


def general_exception_handler(request: Request, exception: Exception):
    sentry_sdk.capture_exception(exception)
    return JSONResponse({'message': "خطایی رخ داده است. لطفا با پشتیبانی تماس بگیرید."}, status_code=500)
