import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Any, get_type_hints
from fastapi import Request
from enum import Enum

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Adjust as needed
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    status_code = 500
    error_message = "Internal Server Error"

    print('bawah',exc)
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        error_message = exc.detail
    else:
        error_message = str(exc)  # Use the exception's string representation

    return JSONResponse(
        status_code=status_code,  # Original status code
        content={
            "error": error_message,  # The error message
            "detail": str(exc)  # Provide the exception message as detail
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    print(exc.status_code)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}

    # Try to parse the incoming request data
    try:
        request_data = await request.json()
    except Exception:
        request_data = {}

    print(exc)

    # Extract the model used for validation from the exception
    for error in exc.errors():
        loc = error["loc"][-1]  # The field name in the model
        msg = error["msg"]

        # Check if it's an Enum validation error and override the message
        if 'enum' in error.get('type', ''):
            # Customize error message for Enum fields
            errors[loc] = f"{loc} doesn't match allowed values."
        else:
            errors[loc] = msg

    # Return the error response in the desired format
    return JSONResponse(
        status_code=400,
        content={
            "error": "Bad Request",
            "detail": errors
        },
    )



