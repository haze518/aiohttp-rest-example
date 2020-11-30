from aiohttp import web

from app.main import create_app

if __name__ == "__main__":
    web_app = create_app()
    web.run_app(web_app)