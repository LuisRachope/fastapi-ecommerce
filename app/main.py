from fastapi import FastAPI

from app.core.config import settings

from app.presentation.api.v1.endpoints.ping import router as ping_router
from app.presentation.api.v1.endpoints.product import router as product_router
from app.infrastructure.database import init_db


def _get_app_args() -> dict:
    return dict(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description=settings.API_DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
    )


def _init_fast_api_app() -> FastAPI:
    app = FastAPI(**_get_app_args())
    app = _config_app_routers(app)

    @app.on_event("startup")
    async def _on_startup():
        await init_db()

    return app


def init_app() -> FastAPI:
    return _init_fast_api_app()


def _config_app_routers(app: FastAPI):
    routers = [
        ping_router,
        product_router,
    ]
    [app.include_router(router) for router in routers]
    return app


app = init_app()
