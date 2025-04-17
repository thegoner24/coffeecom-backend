from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..models.order import Order
from .. import db

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Admin: Get all users
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({'msg': 'Admin access required'}), 403
    users = User.query.all()
    return jsonify([
        {
            'id': u.id,
            'email': u.email,
            'username': u.username,
            'role': u.role
        } for u in users
    ])

# Admin: Delete user
@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user(user_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != 'admin':
        return jsonify({'msg': 'Admin access required'}), 403
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'msg': 'User not found'}), 404
    db.session.delete(target_user)
    db.session.commit()
    return jsonify({'msg': 'User deleted by admin'})

# Admin: Get all orders
@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({'msg': 'Admin access required'}), 403
    orders = Order.query.all()
    return jsonify([
        {
            'id': o.id,
            'user_id': o.user_id,
            'status': o.status,
            'total_amount': o.total_amount
        } for o in orders
    ])

# Admin: Update order status
@admin_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({'msg': 'Admin access required'}), 403
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'msg': 'Order not found'}), 404
    data = request.get_json()
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify({'msg': 'Order status updated'})
