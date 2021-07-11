# Create endpoints
from flask import app
from flask import jsonify
from flask_rest_jsonapi import Api

from apis.future import FutureDetail
from apis.future import FutureList
from apis.option import OptionDetail
from apis.option import OptionList


def register_base_routes(app):
    @app.route("/")
    def index():
        response = "Hello from a public endpoint! You don't need to be authenticated to see this."
        return jsonify(message=response)


def register_json_routes(app):
    api = Api(app)
    api.route(OptionList, "option_list", "/app/options")
    api.route(OptionDetail, "option_detail", "/app/options/<int:id>")
    api.route(FutureList, "future_list", "/app/futures")
    api.route(FutureDetail, "future_detail", "/app/futures/<int:id>")
