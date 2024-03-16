from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY
from backbone.exception.custom_exeptions import UnicornException, unicorn_exception_handler
from backbone.exception.pydantic_validation_exception import validation_exception_handler
from backbone.infrastructure.databases.postgres_connection import DEFAULT_ENGIN, DEFAULT_SESSION_FACTORY
from mapper import mapper_init
from product.entrypoints.routes import router as product_route
from product.migrate_language import migrate_language


@asynccontextmanager
async def lifespan(app: FastAPI):
    mapper_init()
    MAPPER_REGISTRY.metadata.create_all(DEFAULT_ENGIN)
    migrate_language(DEFAULT_SESSION_FACTORY)
    yield


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(UnicornException, unicorn_exception_handler)

app.include_router(product_route)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
