# Тестовое задание

## Перед первым запуском необходимо провести миграцию

~~~~
$ alembic revision --autogenerate -m "Added required tables"
~~~~

~~~~
$ alembic upgrade head
~~~~

## Swagger можно посмотреть по адресу

~~~~
http://localhost:8080/docs
~~~~