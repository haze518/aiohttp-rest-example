from sqlalchemy.sql.expression import literal_column
from datetime import date, datetime
from sqlalchemy import (select,
                        insert,
                        update,
                        delete)

from app.models.db import database
from app.models.models import (TransactionHistory,
                               Limits)
from typing import (List,
                    Mapping,
                    Optional)


# async def check_data_limits(transaction_data: Mapping,
#                             limit_data: Mapping) -> Optional[Mapping]:
#     date_time = datetime.today().replace(microsecond=0)
#     query = (
#         insert(TransactionHistory)
#         .values(
#             client_id=data['client_id'],
#             data=date_time,
#             amount=transaction_data['amount'],
#             currency=data['currency'],
#             country=data['country'],
#             limits_id=data['limit_id']
#         )
#     )
#     return await database.fetch_one(query)
