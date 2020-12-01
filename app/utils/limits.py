from sqlalchemy.sql.expression import literal_column
from sqlalchemy import (select,
                        insert,
                        update,
                        delete)

from app.models.db import database
from app.models.models import Limits
from typing import (List,
                    Mapping,
                    Optional)


async def select_limits_all() -> List[Mapping]:
    query = (
        select([Limits])
    )
    return await database.fetch_all(query)


async def select_limits_client(id_: int) -> Optional[Mapping]:
    query = (
        select([Limits])
        .where(Limits.id == id_)
    )
    return await database.fetch_one(query)


async def check_data_limits(data: Mapping) -> Optional[Mapping]:
    query = (
        select()
        .select_from(Limits)
        .where(Limits.client_id == data['client_id'] and
               Limits.country == data['country'] and
               Limits.currency == data['currency'])
    )
    return await database.fetch_one(query)


async def check_id(id_: int) -> Optional[Mapping]:
    query = (
        select([Limits])
        .where(Limits.id == id_)
    )
    return await database.fetch_one(query)


async def create_new_limit(data: Mapping) -> Optional[Mapping]:
    query = (
        insert(Limits)
        .values(
            client_id=data['client_id'],
            country=data['country'],
            currency=data['currency'],
            max_transfer=data['max_transfer']
        )
        .returning(literal_column('*'))
    )
    return await database.fetch_one(query)


async def update_limit(data: Mapping) -> Optional[Mapping]:
    query = (
        update(Limits)
        .where(Limits.id == data['id'])
        .values(
            client_id=data['client_id'],
            country=data['country'],
            currency=data['currency'],
            max_transfer=data['max_transfer']
        )
        .returning(literal_column('*'))
    )
    return await database.fetch_one(query)


async def delete_limit_by_id(id_: int) -> None:
    query = (
        delete(Limits)
        .where(Limits.id == id_)
    )
    await database.fetch_one(query)
