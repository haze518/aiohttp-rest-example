import logging
from aiohttp import web
from aiohttp_apispec import (
    setup_aiohttp_apispec,
    validation_middleware,
)

from app.routes import setup_routes
from app.models.db import database


def create_app() -> web.Application:
    app = web.Application()
    setup_routes(app)
    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)
    setup_aiohttp_apispec(app, swagger_path="/docs")
    app.middlewares.append(validation_middleware)
    return app


async def startup(app: web.Application) -> None:
    await database.connect()


async def shutdown(app: web.Application) -> None:
    await database.disconnect()
