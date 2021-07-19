from aiohttp import web
from aiohttp_apispec import (
      request_schema,
      docs,
      response_schema,
)
from datetime import datetime
from http import HTTPStatus

from app.models.models import (
      Limits,
      TransactionHistory,
)
from app.schemas import (
      TransactionRequestSchema,
      TransactionResponseSchema,
)
from app.utils import (
      select_all,
      unpack_object_data,
      create_new_object,
      get_new_limit_data,
)


@docs(tags=['Transactions'],
      summary='Внесение операции в историю')
@request_schema(TransactionRequestSchema)
@response_schema(TransactionResponseSchema, code=HTTPStatus.CREATED.value)
async def create_transaction(request):
    data = request['data']
    limit = await get_new_limit_data(Limits, data)
    data['date'] = datetime.today().replace(microsecond=0)
    data.update(limit)
    row = await create_new_object(TransactionHistory, data)
    row = unpack_object_data(row)
    row['date'] = str(row['date'])
    return web.json_response(row)


@docs(tags=['Transactions'],
      summary='Возвратить все данные')
@response_schema(TransactionResponseSchema, code=HTTPStatus.OK.value)
async def transaction_list(request):
    rows = await select_all(TransactionHistory)
    schema = TransactionResponseSchema(many=True)
    limit_json = schema.dump(rows)
    return web.json_response(limit_json)
