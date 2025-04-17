from .. import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(32), default='pending')  # pending, processing, shipped, delivered, cancelled
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.String(256))
    billing_address = db.Column(db.String(256))
    payment_method = db.Column(db.String(32))
    shipping_fee = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tracking_number = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', lazy=True)
