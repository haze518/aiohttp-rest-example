import os
import pytest

# Необходимо создать переменную окружения до импорта db
os.environ['TESTING'] = 'True'

from alembic import command
from alembic.config import Config
from sqlalchemy_utils import create_database, drop_database

from app.models import db
from app.main import create_app


@pytest.fixture
def temp_db():
    """
    Создание БД для тестов
    """
    create_database(db.SQLALCHEMY_DATABASE_URL)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    try:
        yield db.SQLALCHEMY_DATABASE_URL
    finally:
        drop_database(db.SQLALCHEMY_DATABASE_URL)


@pytest.fixture
async def api_client(temp_db, aiohttp_client):
    app = create_app()
    client = await aiohttp_client(app)
    try:
        yield client
    finally:
        await client.close()
