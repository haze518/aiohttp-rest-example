from aiohttp import web

from app.handlers import (limits_list,
                          limits_client,
                          create_limit,
                          change_limit,
                          delete_limit,
                          transaction_list,
                          create_transaction)


def setup_routes(app: web.Application):
    app.router.add_post("/limits", create_limit)
    app.router.add_get("/limits", limits_list)
    app.router.add_put("/limits", change_limit)
    app.router.add_delete("/limits/client/{id:\d+}", delete_limit)
    app.router.add_get("/limits/client/{id:\d+}", limits_client)
    app.router.add_get("/transaction", transaction_list)
    app.router.add_post("/transaction", create_transaction)
