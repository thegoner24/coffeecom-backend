from flask import Blueprint, request, jsonify
from .. import db
from ..models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'msg': 'Missing email or password'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'Email already registered'}), 409
    # Accept role, default to 'user', allow only 'user' or 'seller'
    allowed_roles = ['user', 'seller']
    role = data.get('role', 'user')
    if role not in allowed_roles:
        return jsonify({'msg': 'Invalid role. Allowed roles: user, seller'}), 400
    user = User(
        username=data.get('username', data['email']),
        email=data['email'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        role=role
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User registered successfully', 'role': user.role}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'msg': 'Missing email or password'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'msg': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token, 'user': {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'role': user.role
    }}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role
    })

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    data = request.get_json()
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.username = data.get('username', user.username)
    user.address = data.get('address', user.address)
    user.phone_number = data.get('phone_number', user.phone_number)
    db.session.commit()
    return jsonify({'msg': 'Profile updated'})

@auth_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'Account deleted'})
