from fastapi import FastAPI

from config import settings
from routes import api_router


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Secure customer-support intent API foundation.",
    )
    application.include_router(api_router)
    return application


app = create_app()
