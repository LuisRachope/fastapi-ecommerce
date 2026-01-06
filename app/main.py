from fastapi import FastAPI

from app.presentation.ping import router as ping_router

app = FastAPI(
    title="E-Commerce API",
    version="1.0.0",
    description="API de E-commerce",
    docs_url="/ui",
)

def init_app():
    app = _init_fast_api_app()
    return app

def _init_fast_api_app() -> FastAPI:
    app = FastAPI(**_get_app_args())
    app = _config_app_routers(app)
    return app

def _get_app_args() -> dict:
    return dict(
        title="E-Commerce API",
        version="1.0.0",
        description="API de E-commerce",
        docs_url="/ui",
        redoc_url=None,
    )

def _config_app_routers(app: FastAPI):
    routers = [
        ping_router,
    ]
    [app.include_router(router) for router in routers]
    return app

app = init_app()
