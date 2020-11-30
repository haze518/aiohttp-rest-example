from aiohttp import web
from aiohttp_apispec import (
    setup_aiohttp_apispec,
    validation_middleware,
)

from app.routes import setup_routes
from app.models.db import database


async def create_app():
    app = web.Application()
    setup_routes(app)
    # In-memory toy-database:
    app["users"] = []
    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)
    setup_aiohttp_apispec(app, swagger_path="/docs")
    app.middlewares.append(validation_middleware)
    return app


async def startup(app):
    await database.connect()


async def shutdown(app):
    await database.disconnect()
