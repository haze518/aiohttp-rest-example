from marshmallow import Schema, fields


class LimitsRequestSchema(Schema):
    client_id = fields.Int(required=True)


class LimitsResponseSchema(Schema):
    client_id = fields.Int(required=True)
    country = fields.Str(required=True)
    currency = fields.Str(required=True)
    max_transfer = fields.Int(required=True)


class PostLimitsRequestSchema(LimitsResponseSchema):
    pass


class TransactionRequestSchema(Schema):
    client_id = fields.Int()


class TransactionResponseSchema(Schema):
    client_id = fields.Int()
    date = fields.Date()
    amount = fields.Int()
    currency = fields.Str()
    country = fields.Str()
