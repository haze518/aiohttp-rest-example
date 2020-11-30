from os import environ

import databases

# берем параметры БД из переменных окружения
DB_USER = environ.get("DB_USER", "postgres")
DB_PASSWORD = environ.get("DB_PASSWORD", "ZFv859RzLF6ZmEZN")
DB_HOST = environ.get("DB_HOST", "localhost")
TESTING = environ.get("Testing")
if TESTING:
    DB_NAME = "transaction_test"
else:
    DB_NAME = "transaction"
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
# создаем объект database, который будет использоваться для выполнения запросов
database = databases.Database(SQLALCHEMY_DATABASE_URL)