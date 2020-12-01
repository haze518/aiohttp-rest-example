from aiohttp import web
from http import HTTPStatus
from aiohttp_apispec import (request_schema,
                             docs,
                             response_schema)

from app.schemas import (TransactionRequestSchema,
                         TransactionResponseSchema)
from app.utils.limits import check_id


# @docs(tags=['Limits'],
#       summary='Внесение операции в историю')
# @request_schema(TransactionRequestSchema, locations='query')
# @response_schema(TransactionResponseSchema, code=HTTPStatus.OK.value)
# async def limits_list(request):
#     data = request['data']
#     result = await check_id(data['id'])
#     if result is None:
#         raise web.HTTPNotFound()
#     elif result['max_transfer'] < data['amount']:
#         raise web.HTTPBadRequest(body='Недостаточно средств на счету')
#     result['amount'] = 
    
    
#     schema = LimitsResponseSchema(many=True)
#     limit_json = schema.dump(rows)
#     return web.json_response(limit_json)