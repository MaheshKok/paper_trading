# Create data storage
from datetime import datetime

from extensions import db


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # basic detail
    quantity = db.Column(db.Integer, default=25)
    buy_price = db.Column(db.Float, nullable=False)
    exit_price = db.Column(db.Float, nullable=True)
    profit = db.Column(db.Integer, nullable=True)

    option_type = db.Column(db.String, nullable=False)
    action = db.Column(db.String, nullable=False, server_default="buy")

    strategy = db.Column(db.String, nullable=False)

    order_placed_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, default=datetime.now()
    )
    order_exited_at = db.Column(db.TIMESTAMP(timezone=True), nullable=True)