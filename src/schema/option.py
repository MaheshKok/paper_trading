# Create logical data abstraction (same as data storage for this first example)
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema


class OptionSchema(Schema):
    class Meta:
        type_ = "option"
        self_view = "option_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "option_list"

    id = fields.Integer(as_string=True, dump_only=True)
    quantity = fields.Integer()
    buy_price = fields.Float()
    exit_price = fields.Float()
    order_placed_at = fields.DateTime()
    option_type = fields.String()
    profit = fields.Float()
    strategy = fields.String()
    updated_at = fields.DateTime()
    action = fields.String()
