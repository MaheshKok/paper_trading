from flask import Flask

from extensions import register_extensions
from views import register_base_routes
from views import register_json_routes


def _create_app():
    """Base Flask app factory used by all apps."""
    # Create the Flask application
    app = Flask(__name__, instance_relative_config=False)
    register_extensions(app)
    return app


def create_webapp() -> Flask:  # pragma: no cover
    """
    Create a version of the app suitable for serving the website locally or in production.
    """
    app = _create_app()
    register_json_routes(app)
    register_base_routes(app)
    return app



# below code to fetch option chain data
import requests

requests.get(
    "https://vbiz.in/optionchain/foc.php?symbol=NIFTY&expiry=15JUL2021",
    headers={
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,mr-IN;q=0.6,mr;q=0.5,en-GB;q=0.4,en-US;q=0.3",
        "origin": "http://vbiz.in",
        "referer": "http://vbiz.in/",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    },
)
