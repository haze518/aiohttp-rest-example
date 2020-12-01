"""
Модуль содержит схемы для валидации данных в запросах и ответах.
"""
from marshmallow import Schema, fields
from marshmallow.validate import Length


class Base(Schema):
    class Meta:
        ordered = True
        

class PostLimitsRequestSchema(Base):
    client_id = fields.Int(required=True)
    country = fields.Str(validate=Length(equal=3), required=True)
    currency = fields.Str(validate=Length(equal=3), required=True)
    max_transfer = fields.Int(required=True)


class PostLimitsReponseSchema(Base):
    id = fields.Int(required=True)
    client_id = fields.Int(required=True)
    country = fields.Str(required=True)
    currency = fields.Str(required=True)
    max_transfer = fields.Int(required=True)


class PutLimitsRequestSchema(Base):
    id = fields.Int(required=True)
    client_id = fields.Int(required=True)
    country = fields.Str(validate=Length(equal=3), required=True)
    currency = fields.Str(validate=Length(equal=3), required=True)
    max_transfer = fields.Int(required=True)


class PutLimitsResponseSchema(Base):
    id = fields.Int(required=True)
    client_id = fields.Int(required=True)
    country = fields.Str(required=True)
    currency = fields.Str(required=True)
    max_transfer = fields.Int(required=True)


class DeleteLimitsResponseSchema(Base):
    message = fields.Str()


class LimitsResponseSchema(Base):
    id = fields.Int(required=True)
    client_id = fields.Int(required=True)
    country = fields.Str(required=True)
    currency = fields.Str(required=True)
    max_transfer = fields.Int(required=True)



# class TransactionRequestSchema(Schema):
#     client_id = fields.Int()


# class TransactionResponseSchema(Schema):
#     client_id = fields.Int()
#     date = fields.Date()
#     amount = fields.Int()
#     currency = fields.Str()
#     country = fields.Str()
