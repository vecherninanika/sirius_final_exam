from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from webapp.api import ingredient_router
from webapp.metrics import metrics
from webapp.logger import LogServerMiddleware
from webapp.metrics import MeasureLatencyMiddleware


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(LogServerMiddleware)
    app.add_middleware(MeasureLatencyMiddleware)

    # CORS Middleware should be the last.
    # See https://github.com/tiangolo/fastapi/issues/1663 .
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],    # CORS разрешено для всех доменов.
        allow_credentials=True, # Разрешает использование cookie в cross-origin запросах
        allow_methods=['*'],    # Разрешает все HTTP методы
        allow_headers=['*'],
    )


def setup_routers(app: FastAPI) -> None:
    app.add_route('/metrics', metrics)

    app.include_router(ingredient_router)


def create_app() -> FastAPI:
    app = FastAPI()

    setup_middleware(app)
    setup_routers(app)
    Instrumentator().instrument(app).expose(app)

    return app

