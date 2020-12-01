from sqlalchemy.sql.expression import literal_column
from aiohttp import web
from sqlalchemy import (select,
                        insert,
                        update,
                        delete)

from app.models.db import database


async def select_all(table):
    query = (
        select([table])
    )
    return await database.fetch_all(query)


async def select_by_id(table, id_):
    query = (
        select([table])
        .where(table.id == id_)
    )
    return await database.fetch_one(query)


async def check_data_exists(table, data):
    query = (
        select()
        .select_from(table)
        .where(table.client_id == data['client_id'] and
               table.country == data['country'] and
               table.currency == data['currency'])
    )
    return await database.fetch_one(query)


async def create_new_object(table, data):
    new_data = get_table_attrs(table, data)
    query = (
        insert(table)
        .values(**new_data)
        .returning(literal_column('*'))
    )
    return await database.fetch_one(query)


async def update_existing_object(table, data):
    new_data = get_table_attrs(table, data)
    query = (
        update(table)
        .where(table.id == data['id'])
        .values(**new_data)
        .returning(literal_column('*'))
    )
    return await database.fetch_one(query)


async def delete_existing_object(table, id_):
    query = (
        delete(table)
        .where(table.id == id_)
    )
    await database.fetch_one(query)


def get_table_attrs(table, data):
    """
    Возвратить названия столбцов класса sqlalchemy
    """
    table_columns = set(table.__table__.columns.keys())
    table_columns.discard('id')
    return dict((k, v) for k, v in data.items() if k in table_columns)


def unpack_object_data(data):
    """
    Распаковка данных из выгруженного с БД объекта
    """
    return dict(zip(data, data.values()))


async def check_not_found(table, id_):
    """
    Проверка, имеется ли объект с таким id в БД
    """
    result = await select_by_id(table, id_)
    if result is None:
        raise web.HTTPNotFound()
    return result


def check_insufficient_funds(limit, data):
    """
    Проверка остатка на балансе
    """
    if limit['max_transfer'] < data['amount']:
        raise web.HTTPBadRequest(reason='INSUFFICIENT FUNDS')


async def update_account_balance(table, limit, data):
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


async def get_new_limit_data(table, data):
    """
    Возвратить значение обновленного лимита
    """
    limits = await check_not_found(table, data['limit_id'])
    limits = unpack_object_data(limits)
    return await update_account_balance(table, limits, data)
