from os import environ

import databases

# берем параметры БД из переменных окружения
DB_USER = environ.get("POSTGRES_USER")
DB_PASSWORD = environ.get("POSTGRES_PASSWORD")
DB_HOST = environ.get("POSTGRES_HOST")
TESTING = environ.get("Testing")
if TESTING:
    DB_NAME = "transaction_test"
else:
    DB_NAME = environ.get("POSTGRES_DB")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
# создаем объект database, который будет использоваться для выполнения запросов
database = databases.Database(SQLALCHEMY_DATABASE_URL)
