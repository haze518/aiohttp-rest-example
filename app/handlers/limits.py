from aiohttp import web
from aiohttp.web_response import Response
from aiohttp_apispec import (request_schema,
                             docs,
                             response_schema)
from sqlalchemy import select, insert
from http import HTTPStatus
import json

from app.models.db import database
from app.models.models import Limits
from app.schemas import (LimitsResponseSchema,
                         LimitsRequestSchema,
                         PostLimitsRequestSchema)


@docs(tags=['Limits'],
      summary='Возвратить все данные с таблицы по лимитам')
@response_schema(LimitsResponseSchema, code=HTTPStatus.OK.value)
async def limits_list(request):
    query = (
        select([
            Limits.client_id,
            Limits.country,
            Limits.currency,
            Limits.max_transfer
        ])
        .select_from(Limits)
    )
    rows = await database.fetch_all(query)
    schema = LimitsResponseSchema(many=True)
    limit_json = schema.dump(rows)
    return web.json_response(limit_json)


@docs(tags=['Limits'],
      summary='Возвратить данные по лимитам, по id клиенту')
@response_schema(LimitsResponseSchema, code=HTTPStatus.OK.value)
async def limits_client(request):
    data = int(request.match_info.get('client_id'))
    query = (
        select([
            Limits.client_id,
            Limits.country,
            Limits.currency,
            Limits.max_transfer
        ])
        .select_from(Limits)
        .where(Limits.client_id == data)
    )
    rows = await database.fetch_all(query)
    if not len(rows):
        raise web.HTTPNotFound()
    schema = LimitsResponseSchema(many=True)
    limit_json = schema.dump(rows)
    return web.json_response(limit_json)


@docs(tags=['Limits'],
      summary='Отправить данные по лимитам')
@request_schema(PostLimitsRequestSchema, location='query')
@response_schema(LimitsResponseSchema, code=HTTPStatus.CREATED.value)
async def create_limit(request):
    data = request['data']
    query = (
        insert(Limits)
        .values(
            client_id=data['client_id'],
            country=data['country'],
            currency=data['currency'],
            max_transfer=data['max_transfer']
        )
        .returning(
            Limits.client_id,
            Limits.currency,
            Limits.country,
            Limits.max_transfer
        )
    )
    post = await database.fetch_one(query)
    post = dict(zip(post, post.values()))
    return web.json_response(post)
