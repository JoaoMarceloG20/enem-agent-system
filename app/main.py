from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.api.main import api_router
from app.core.config import settings
from app.api.models import ValidationErrorResponse, ValidationErrorDetail, ErrorResponse, StatusEnum


def custom_generate_unique_id(route: APIRoute) -> str:
    return f'{route.tags[0]}-{route.name}'


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f'{settings.API_V1_STR}/openapi.json'
    if settings.DOCS_ENABLED
    else None,
    docs_url='/docs' if settings.DOCS_ENABLED else None,
    redoc_url='/redoc' if settings.DOCS_ENABLED else None,
    generate_unique_id_function=custom_generate_unique_id,
)


# Exception handlers for structured error responses
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with structured response"""
    validation_errors = []
    
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        validation_errors.append(
            ValidationErrorDetail(
                field=field,
                message=error["msg"],
                invalid_value=error.get("input")
            )
        )
    
    response = ValidationErrorResponse(
        status=StatusEnum.ERROR,
        message="Validation error in request data",
        validation_errors=validation_errors
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.model_dump(mode='json')
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors"""
    validation_errors = []
    
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        validation_errors.append(
            ValidationErrorDetail(
                field=field,
                message=error["msg"],
                invalid_value=error.get("input")
            )
        )
    
    response = ValidationErrorResponse(
        status=StatusEnum.ERROR,
        message="Data validation error",
        validation_errors=validation_errors
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.model_dump(mode='json')
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with structured response"""
    response = ErrorResponse(
        status=StatusEnum.ERROR,
        message="An unexpected error occurred",
        error_code="INTERNAL_SERVER_ERROR",
        details={
            "error_type": type(exc).__name__,
            "path": str(request.url.path),
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(mode='json')
    )


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
