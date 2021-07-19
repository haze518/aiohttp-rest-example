import argparse
from aiohttp import web

from app.main import create_app

parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('--host', type=str)
parser.add_argument('--port', type=int)

if __name__ == "__main__":
    args = parser.parse_args()
    web_app = create_app()
    web.run_app(web_app, host=args.host, port=args.port)
