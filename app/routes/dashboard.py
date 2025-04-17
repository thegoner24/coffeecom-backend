from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..models.order import Order
from ..models.product import Product
from ..models.transaction import Transaction
from .. import db

from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/user', methods=['GET'])
@jwt_required()
def user_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    orders = Order.query.filter_by(user_id=user_id).count()
    transactions = Transaction.query.filter_by(user_id=user_id).count()
    return jsonify({
        'orders_count': orders,
        'transactions_count': transactions,
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role
        }
    })

@dashboard_bp.route('/seller', methods=['GET'])
@jwt_required()
def seller_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'seller':
        return jsonify({'msg': 'Seller access required'}), 403
    products_count = Product.query.filter_by().count()  # Optionally, filter by seller_id if implemented
    # Optionally, add more seller stats
    return jsonify({
        'products_count': products_count,
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role
        }
    })

@dashboard_bp.route('/admin', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({'msg': 'Admin access required'}), 403
    users_count = User.query.count()
    orders_count = Order.query.count()
    products_count = Product.query.count()
    transactions_count = Transaction.query.count()
    return jsonify({
        'users_count': users_count,
        'orders_count': orders_count,
        'products_count': products_count,
        'transactions_count': transactions_count
    })
