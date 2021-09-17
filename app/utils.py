from typing import List, Optional

from aiohttp import web
from databases.backends.postgres import Record
from sqlalchemy import (
    select,
    insert,
    update,
    delete,
)
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql.expression import literal_column

from app.models.db import database


async def select_all(table: DeclarativeMeta) -> List[Record]:
    query = (
        select([table])
    )
    return await database.fetch_all(query)


async def select_by_id(table: DeclarativeMeta, id_) -> Optional[Record]:
    query = (
        select([table])
        .where(table.id == id_)
    )
    return await database.fetch_one(query)


async def check_data_exists(table: DeclarativeMeta, data: dict) -> Optional[Record]:
    query = (
        select()
        .select_from(table)
        .where(table.client_id == data['client_id'] and
               table.country == data['country'] and
               table.currency == data['currency'])
    )
    return await database.fetch_one(query)


async def create_new_object(table: DeclarativeMeta, data: dict) -> Optional[Record]:
    new_data = get_table_attrs(table, data)
    query = (
        insert(table)
        .values(**new_data)
        .returning(literal_column('*'))
    )
    return await database.fetch_one(query)


async def update_existing_object(table: DeclarativeMeta, data: dict) -> Optional[Record]:
    new_data = get_table_attrs(table, data)
    query = (
        update(table)
        .where(table.id == data['id'])
        .values(**new_data)
        .returning(literal_column('*'))
    )
    return await database.fetch_one(query)


async def delete_existing_object(table: DeclarativeMeta, id_: int) -> Optional[Record]:
    query = (
        delete(table)
        .where(table.id == id_)
    )
    await database.fetch_one(query)


def get_table_attrs(table: DeclarativeMeta, data: dict) -> dict:
    """
    Возвратить названия столбцов класса sqlalchemy
    """
    table_columns = set(table.__table__.columns.keys())
    table_columns.discard('id')
    return dict((k, v) for k, v in data.items() if k in table_columns)


def unpack_object_data(data: dict) -> dict:
    """
    Распаковка данных из выгруженного с БД объекта
    """
    return dict(zip(data, data.values()))


async def check_not_found(table: DeclarativeMeta, id_: int) -> Optional[Record]:
    """
    Проверка, имеется ли объект с таким id в БД
    """
    result = await select_by_id(table, id_)
    if result is None:
        raise web.HTTPNotFound()
    return result


def check_insufficient_funds(limit: int, data: dict) -> None:
    """
    Проверка остатка на балансе
    """
    if limit['max_transfer'] < data['amount']:
        raise web.HTTPBadRequest(reason='INSUFFICIENT FUNDS')


async def update_account_balance(table: DeclarativeMeta, limit: int, data: dict) -> int:
    """
    Обновить баланс счета
    """
    check_insufficient_funds(limit, data)
    limit['max_transfer'] -= data['amount']
    if limit['max_transfer'] == 0:
        await delete_existing_object(table, data['limit_id'])
    else:
        await update_existing_object(table, limit)
    return limit


async def get_new_limit_data(table: DeclarativeMeta, data: dict) -> int:
    """
    Возвратить значение обновленного лимита
    """
    limits = await check_not_found(table, data['limit_id'])
    limits = unpack_object_data(limits)
    return await update_account_balance(table, limits, data)
