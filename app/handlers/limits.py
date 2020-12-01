from aiohttp import web
from aiohttp_apispec import (request_schema,
                             docs,
                             response_schema)
from http import HTTPStatus

from app.schemas import (LimitsResponseSchema,
                         PostLimitsRequestSchema,
                         PostLimitsReponseSchema,
                         PutLimitsRequestSchema,
                         PutLimitsResponseSchema,
                         DeleteLimitsResponseSchema)
from app.utils.limits import (select_limits_all,
                              select_limits_client,
                              check_id,
                              check_data_limits,
                              create_new_limit,
                              update_limit,
                              delete_limit_by_id)


@docs(tags=['Limits'],
      summary='Возвратить все данные')
@response_schema(LimitsResponseSchema, code=HTTPStatus.OK.value)
async def limits_list(request):
    rows = await select_limits_all()
    schema = LimitsResponseSchema(many=True)
    limit_json = schema.dump(rows)
    return web.json_response(limit_json)


@docs(tags=['Limits'],
      summary='Возвратить данные по id клиенту')
@response_schema(LimitsResponseSchema, code=HTTPStatus.OK.value)
async def limits_client(request):
    id_ = int(request.match_info.get('id'))
    rows = await select_limits_client(id_)
    if rows is None:
        raise web.HTTPNotFound()
    schema = LimitsResponseSchema()
    limit_json = schema.dump(rows)
    return web.json_response(limit_json)


@docs(tags=['Limits'],
      summary='Отправить данные')
@request_schema(PostLimitsRequestSchema, location='query')
@response_schema(PostLimitsReponseSchema, code=HTTPStatus.CREATED.value)
async def create_limit(request):
    data = request['data']
    result = await check_data_limits(data)
    if result is not None:
        raise web.HTTPBadRequest()
    post = await create_new_limit(data)
    post = dict(zip(post, post.values()))
    return web.json_response(post)


@docs(tags=['Limits'],
      summary='Изменить существующую запись')
@request_schema(PutLimitsRequestSchema, location='query')
@response_schema(PutLimitsResponseSchema, code=HTTPStatus.OK.value)
async def change_limit(request):
    data = request['data']
    result = await check_id(data['id'])
    if result is None:
        raise web.HTTPNotFound()
    post = await update_limit(data)
    post = dict(zip(post, post.values()))
    return web.json_response(post)


@docs(tags=['Limits'],
      summary='Удалить запись по id')
@response_schema(DeleteLimitsResponseSchema, code=HTTPStatus.NO_CONTENT.value)
async def delete_limit(request):
    id_ = int(request.match_info.get('id'))
    result = await check_id(id_)
    if result is None:
        raise web.HTTPNotFound()
    await delete_limit_by_id(id_)
    return web.json_response({'message': 'Запись успешно удалена'})
