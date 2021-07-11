from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema


class FutureSchema(Schema):
    class Meta:
        type_ = "future"
        self_view = "future_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "future_list"

    id = fields.Integer(as_string=True, dump_only=True)
    quantity = fields.Integer(required=True, load_only=True)
    action = fields.String()
    buy_price = fields.Float(load_only=True)
    exit_price = fields.Float(load_only=True)
    created_at = fields.DateTime()
