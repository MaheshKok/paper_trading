# Create resource managers
import logging
from datetime import datetime

import nsepython
from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from extensions import db
from models.option import Option
from schema.option import OptionSchema

log = logging.getLogger(__file__)


class OptionDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get("computer_id") is not None:
            try:
                computer = (
                    self.session.query(Option)
                    .filter_by(id=view_kwargs["computer_id"])
                    .one()
                )
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "computer_id"},
                    "Computer: {} not found".format(view_kwargs["computer_id"]),
                )
            else:
                if computer.person is not None:
                    view_kwargs["id"] = computer.person.id
                else:
                    view_kwargs["id"] = None

    schema = OptionSchema
    data_layer = {
        "session": db.session,
        "model": Option,
        "methods": {"before_get_object": before_get_object},
    }


class OptionList(ResourceList):
    def before_post(self, args, kwargs, data=None):

        if data["option_type"] == "PE":

            last_trade_list = Option.query.order_by(Option.created_at.desc()).all()
            if last_trade_list:
                last_trade = last_trade_list[0]
                exit_price = nsepython.nse_quote_ltp(
                    "BANKNIFTY", "24-Jun-2021", "CE", 34500
                )
                last_trade.profit = exit_price - last_trade.buy_price
                last_trade.exit_price = exit_price
                last_trade.updated_at = datetime.now()
                db.session.add(last_trade)
                db.session.commit()

            data["buy_price"] = nsepython.nse_quote_ltp(
                "BANKNIFTY", "24-Jun-2021", "PE", 34500
            )
        else:
            last_trade_list = Option.query.order_by(Option.created_at.desc()).all()
            if last_trade_list:
                last_trade = last_trade_list[0]
                exit_price = nsepython.nse_quote_ltp(
                    "BANKNIFTY", "24-Jun-2021", "PE", 34500
                )
                last_trade.exit_price = exit_price
                last_trade.profit = exit_price - last_trade.buy_price
                last_trade.updated_at = datetime.now()
                db.session.add(last_trade)
                db.session.commit()

            data["buy_price"] = nsepython.nse_quote_ltp(
                "BANKNIFTY", "24-Jun-2021", "CE", 34500
            )

    schema = OptionSchema
    data_layer = {
        "session": db.session,
        "model": Option,
    }
