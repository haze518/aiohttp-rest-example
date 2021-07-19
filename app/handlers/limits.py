from aiohttp import web
from aiohttp_apispec import (
    request_schema,
    docs,
    response_schema,
)
from http import HTTPStatus

from app.models.models import Limits
from app.schemas import (
    LimitsResponseSchema,
    PostLimitsRequestSchema,
    PostLimitsReponseSchema,
    PutLimitsRequestSchema,
    PutLimitsResponseSchema,
    DeleteLimitsResponseSchema,
)
from app.utils import (
    select_all,
    check_data_exists,
    create_new_object,
    update_existing_object,
    delete_existing_object,
    unpack_object_data,
    check_not_found,
)


@docs(tags=['Limits'],
      summary='Возвратить все данные')
@response_schema(LimitsResponseSchema, code=HTTPStatus.OK.value)
async def limits_list(request):
    rows = await select_all(Limits)
    schema = LimitsResponseSchema(many=True)
    limit_json = schema.dump(rows)
    return web.json_response(limit_json)


@docs(tags=['Limits'],
      summary='Возвратить данные по id клиенту')
@response_schema(LimitsResponseSchema, code=HTTPStatus.OK.value)
async def limits_client(request):
    id_ = int(request.match_info.get('id'))
    result = await check_not_found(Limits, id_)
    schema = LimitsResponseSchema()
    limit_json = schema.dump(result)
    return web.json_response(limit_json)


@docs(tags=['Limits'],
      summary='Отправить данные')
@request_schema(PostLimitsRequestSchema)
@response_schema(PostLimitsReponseSchema, code=HTTPStatus.CREATED.value)
async def create_limit(request):
    data = request['data']
    result = await check_data_exists(Limits, data)
    if result is not None:
        raise web.HTTPBadRequest()
    post = await create_new_object(Limits, data)
    post = unpack_object_data(post)
    return web.json_response(post)


@docs(tags=['Limits'],
      summary='Изменить существующую запись')
@request_schema(PutLimitsRequestSchema)
@response_schema(PutLimitsResponseSchema, code=HTTPStatus.OK.value)
async def change_limit(request):
    data = request['data']
    await check_not_found(Limits, data['id'])
    post = await update_existing_object(Limits, data)
    post = unpack_object_data(post)
    return web.json_response(post)


@docs(tags=['Limits'],
      summary='Удалить запись по id')
@response_schema(DeleteLimitsResponseSchema, code=HTTPStatus.NO_CONTENT.value)
async def delete_limit(request):
    id_ = int(request.match_info.get('id'))
    await check_not_found(Limits, id_)
    await delete_existing_object(Limits, id_)
    return web.json_response({'message': 'Запись успешно удалена'})
