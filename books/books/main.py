import sys

import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from books.core.config import get_settings
from books.core.errors import CustomValidationError
from books.routers import route as books_route

route = APIRouter()

settings_ = get_settings()


def create_app() -> FastAPI:
    logger.remove(0)
    logger.add(sys.stderr, level="TRACE")

    origins = settings_.origin.split()
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.warning(f'Debug mode is {settings_.debug}')
    app.include_router(books_route)
    __version__ = "1.0.0"  # Application version

    return app


app = create_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": str(exc)},
    )


@app.exception_handler(CustomValidationError)
async def custom_validation_error_handler(
        request: Request,
        exc: CustomValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": exc.args[0][1],
            "number": exc.args[0][0]
        },
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
