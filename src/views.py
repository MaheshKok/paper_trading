# Create endpoints
from flask import app
from flask import jsonify
from flask_rest_jsonapi import Api

from apis.nfo import NFODetail
from apis.nfo import NFOList


def register_base_routes(app):
    @app.route("/")
    def index():
        response = "Hello from a public endpoint! You don't need to be authenticated to see this."
        return jsonify(message=response)


def register_json_routes(app):
    api = Api(app)

    # Expected Payload
    {
        "strategy": 1,  # mandatory
        "nfo_type": "option",  # mandatory for now
        "option_type": "ce",  # mandatory for now
        "action": "buy",  # mandatory
        "strike_price": 550,  # if not provided ATM strike price will be picked
        "symbol": "BANKNIFTY",  # its optional,
    }

    api.route(NFOList, "nfo_list", "/api/nfo")
    api.route(NFODetail, "nfo_detail", "/api/nfo/<int:id>")
