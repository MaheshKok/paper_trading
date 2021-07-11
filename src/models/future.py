from datetime import datetime

from extensions import db


class Future(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String)
    quantity = db.Column(db.Integer, default=25)
    buy_price = db.Column(db.Float, nullable=False)
    exit_price = db.Column(db.Float, nullable=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
