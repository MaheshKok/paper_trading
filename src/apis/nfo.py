# Create resource managers
import logging
from datetime import datetime

from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from apis.constants import fetch_data
from extensions import db
from models.nfo import NFO
from schema.nfo import NFOSchema

log = logging.getLogger(__file__)


class NFODetail(ResourceDetail):
    # ignore below code its dummy
    def before_get_object(self, view_kwargs):
        if view_kwargs.get("computer_id") is not None:
            try:
                computer = (
                    self.session.query(NFO)
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

    schema = NFOSchema
    data_layer = {
        "session": db.session,
        "model": NFO,
        "methods": {"before_get_object": before_get_object},
    }


class NFOList(ResourceList):
    def before_post(self, args, kwargs, data=None):
        if data["nfo_type"] == "option":
            last_trade_list = (
                NFO.query.filter_by(strategy=data["strategy"])
                .order_by(NFO.order_placed_at.desc())
                .all()
            )
            # TODO fetch expiry from nse lib
            res = fetch_data(data["symbol"])
            data_lst = res.json()["OptionChainInfo"]
            strike_price = data.get("strike_price")
            strike = data.get("strike")
            option_type = data["option_type"]
            last_trade = False

            if last_trade_list:
                last_trade = last_trade_list[0]
                last_trade_call_put = "ce" if last_trade.option_type == "buy" else "pe"

            if strike:
                for option_data in data_lst:
                    if option_data["strike"] == strike:
                        data["entry_price"] = option_data[f"{option_type}ltp"]
                        break
                    if last_trade and option_data["strike"] == last_trade.strike:
                        exit_price = option_data[f"{last_trade_call_put}ltp"]

            elif strike_price:
                for option_data in data_lst:
                    ltp = int(option_data[f"{option_type}ltp"])
                    diff = ltp - int(data["strike_price"])
                    if diff > -50:
                        data["entry_price"] = option_data[f"{option_type}ltp"]
                        data["strike"] = option_data["strike"]
                        del data["strike_price"]
                        break
                    if last_trade and data["strike"] == last_trade.strike:
                        exit_price = data[f"{last_trade_call_put}ltp"]

            else:
                for option_data in data_lst:
                    if option_data[f"{option_type}status"] == "ATM":
                        data["entry_price"] = option_data[f"{option_type}ltp"]
                        data["strike"] = option_data["strike"]
                        break
                    if last_trade and option_data["strike"] == last_trade.strike:
                        exit_price = option_data[f"{last_trade_call_put}ltp"]

            if last_trade_list:
                last_trade.profit = exit_price - last_trade.entry_price
                last_trade.exit_price = exit_price
                last_trade.updated_at = datetime.now()

                db.session.add(last_trade)
                db.session.commit()

        # do not remove below code
        # if data["option_type"] == "PE":
        #     pass
        # else:
        #     last_trade_list = Option.query.order_by(Option.created_at.desc()).all()
        #     if last_trade_list:
        #         last_trade = last_trade_list[0]
        #         exit_price = nsepython.nse_quote_ltp(
        #             "BANKNIFTY", "24-Jun-2021", "PE", 34500
        #         )
        #         last_trade.exit_price = exit_price
        #         last_trade.profit = exit_price - last_trade.entry_price
        #         last_trade.updated_at = datetime.now()
        #         db.session.add(last_trade)
        #         db.session.commit()
        #
        #     data["entry_price"] = nsepython.nse_quote_ltp(
        #         "BANKNIFTY", "24-Jun-2021", "CE", 34500
        #     )

    schema = NFOSchema
    data_layer = {
        "session": db.session,
        "model": NFO,
    }


# Expected Payload
{
    "strategy": 1,  # mandatory
    "nfo_type": "option",  # mandatory for now
    "option_type": "ce",   # mandatory for now
    "action": "buy",       # mandatory
    "strike_price": 550,  # if not provided ATM strike price will be picked
    "symbol": "BANKNIFTY",  # its optional,
}
