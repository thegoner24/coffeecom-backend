from flask import Blueprint, request, jsonify
from .. import db
from ..models.product import Product
from ..models.category import Category
from flask_jwt_extended import jwt_required, get_jwt_identity

product_bp = Blueprint('product', __name__, url_prefix='/api/products')

@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'category_id': p.category_id,
            'image_url': p.image_url,
            'is_available': p.is_available,
            'discount_percentage': p.discount_percentage,
            'weight': p.weight,
            'dimensions': p.dimensions
        } for p in products
    ])

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'msg': 'Product not found'}), 404
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'category_id': product.category_id,
        'image_url': product.image_url,
        'is_available': product.is_available,
        'discount_percentage': product.discount_percentage,
        'weight': product.weight,
        'dimensions': product.dimensions
    })

@product_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'seller':
        return jsonify({'msg': 'Seller access required'}), 403
    data = request.get_json()
    product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        category_id=data.get('category_id'),
        image_url=data.get('image_url'),
        is_available=data.get('is_available', True),
        discount_percentage=data.get('discount_percentage', 0.0),
        weight=data.get('weight'),
        dimensions=data.get('dimensions')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'msg': 'Product created', 'id': product.id}), 201

@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'msg': 'Product not found'}), 404
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.category_id = data.get('category_id', product.category_id)
    product.image_url = data.get('image_url', product.image_url)
    product.is_available = data.get('is_available', product.is_available)
    product.discount_percentage = data.get('discount_percentage', product.discount_percentage)
    product.weight = data.get('weight', product.weight)
    product.dimensions = data.get('dimensions', product.dimensions)
    db.session.commit()
    return jsonify({'msg': 'Product updated'})

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'msg': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'msg': 'Product deleted'})
