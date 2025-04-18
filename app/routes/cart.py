from flask import Blueprint, request, jsonify
from .. import db
from ..models.user import User
from ..models.product import Product
from ..models.cart import Cart
from ..models.cart_item import CartItem
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    # Get the user's cart or create one if it doesn't exist
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'items': [], 'total': 0.0}), 200
    
    # Get all items in the cart
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    items = []
    total = 0.0
    
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            # Calculate item price with any discounts
            price = product.price
            if product.discount_percentage > 0:
                price = price * (1 - (product.discount_percentage / 100))
            
            item_total = price * item.quantity
            total += item_total
            
            items.append({
                'id': item.id,
                'product_id': product.id,
                'name': product.name,
                'price': price,
                'quantity': item.quantity,
                'item_total': item_total,
                'image_url': product.image_url
            })
    
    return jsonify({
        'items': items,
        'total': total
    })

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Only regular users can add to cart, not sellers
    if user.role == 'seller':
        return jsonify({'msg': 'Sellers cannot purchase products'}), 403
    
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # Validate product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'msg': 'Product not found'}), 404
    
    # Check if product is available
    if not product.is_available:
        return jsonify({'msg': 'Product is not available'}), 400
    
    # Get or create cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        # Update quantity
        cart_item.quantity += quantity
    else:
        # Add new item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'msg': 'Product added to cart'}), 201

@cart_bp.route('/update/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Only regular users can update cart, not sellers
    if user.role == 'seller':
        return jsonify({'msg': 'Sellers cannot purchase products'}), 403
    
    data = request.get_json()
    quantity = data.get('quantity', 1)
    
    # Get user's cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'msg': 'Cart not found'}), 404
    
    # Get cart item
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not cart_item:
        return jsonify({'msg': 'Item not found in cart'}), 404
    
    if quantity <= 0:
        # Remove item if quantity is 0 or negative
        db.session.delete(cart_item)
    else:
        # Update quantity
        cart_item.quantity = quantity
    
    db.session.commit()
    return jsonify({'msg': 'Cart updated'})

@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    user_id = get_jwt_identity()
    
    # Get user's cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'msg': 'Cart not found'}), 404
    
    # Get cart item
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not cart_item:
        return jsonify({'msg': 'Item not found in cart'}), 404
    
    # Remove item
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'msg': 'Item removed from cart'})

@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    user_id = get_jwt_identity()
    
    # Get user's cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'msg': 'Cart not found'}), 404
    
    # Remove all items
    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()
    
    return jsonify({'msg': 'Cart cleared'})
