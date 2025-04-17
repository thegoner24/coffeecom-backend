from .. import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(32), default='pending')  # pending, completed, failed, refunded
    payment_method = db.Column(db.String(32))
    payment_id = db.Column(db.String(128))  # from payment gateway
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order = db.relationship('Order', backref='transactions')
    user = db.relationship('User', backref='transactions')
