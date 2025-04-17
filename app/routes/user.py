from flask import Blueprint, request, jsonify
from .. import db
from ..models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([
        {
            'id': u.id,
            'email': u.email,
            'username': u.username,
            'role': u.role
        } for u in users
    ])

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'role': user.role
    })

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.address = data.get('address', user.address)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify({'msg': 'User updated'})

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'User deleted'})
