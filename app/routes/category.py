from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models.category import Category
from ..models.user import User

category_bp = Blueprint('category', __name__, url_prefix='/api/categories')

@category_bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'seller':
        return jsonify({'msg': 'Seller access required'}), 403
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    if not name:
        return jsonify({'msg': 'Category name is required'}), 400
    if Category.query.filter_by(name=name).first():
        return jsonify({'msg': 'Category already exists'}), 409
    category = Category(name=name, description=description)
    db.session.add(category)
    db.session.commit()
    return jsonify({'msg': 'Category created', 'id': category.id}), 201

@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([
        {
            'id': c.id,
            'name': c.name,
            'description': c.description
        } for c in categories
    ])

@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'msg': 'Category not found'}), 404
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    })

@category_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'seller':
        return jsonify({'msg': 'Seller access required'}), 403
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'msg': 'Category not found'}), 404
    data = request.get_json()
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    db.session.commit()
    return jsonify({'msg': 'Category updated'})

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'seller':
        return jsonify({'msg': 'Seller access required'}), 403
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'msg': 'Category not found'}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({'msg': 'Category deleted'})
