from flask import Blueprint, request, jsonify
from .. import db
from ..models.user import User
from ..models.cart import Cart
from ..models.cart_item import CartItem
from ..models.order import Order
from ..models.order_item import OrderItem
from ..models.product import Product
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

order_bp = Blueprint('order', __name__, url_prefix='/api/orders')

@order_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    
    result = []
    for order in orders:
        order_items = OrderItem.query.filter_by(order_id=order.id).all()
        items = []
        
        for item in order_items:
            product = Product.query.get(item.product_id)
            if product:
                items.append({
                    'id': item.id,
                    'product_id': product.id,
                    'name': product.name,
                    'price': item.price,
                    'quantity': item.quantity,
                    'total': item.price * item.quantity
                })
        
        result.append({
            'id': order.id,
            'order_number': order.order_number,
            'status': order.status,
            'total': order.total,
            'created_at': order.created_at,
            'items': items
        })
    
    return jsonify(result)

@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    
    if not order:
        return jsonify({'msg': 'Order not found'}), 404
    
    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    items = []
    
    for item in order_items:
        product = Product.query.get(item.product_id)
        if product:
            items.append({
                'id': item.id,
                'product_id': product.id,
                'name': product.name,
                'price': item.price,
                'quantity': item.quantity,
                'total': item.price * item.quantity
            })
    
    result = {
        'id': order.id,
        'order_number': order.order_number,
        'status': order.status,
        'total': order.total,
        'shipping_address': order.shipping_address,
        'payment_method': order.payment_method,
        'created_at': order.created_at,
        'items': items
    }
    
    return jsonify(result)

@order_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Only regular users can place orders, not sellers
    if user.role == 'seller':
        return jsonify({'msg': 'Sellers cannot place orders'}), 403
    
    # Get user's cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        return jsonify({'msg': 'Cart is empty'}), 400
    
    data = request.get_json()
    shipping_address = data.get('shipping_address')
    payment_method = data.get('payment_method')
    
    if not shipping_address or not payment_method:
        return jsonify({'msg': 'Shipping address and payment method are required'}), 400
    
    # Calculate order total
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    total = 0.0
    
    # Check if all products are available
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if not product or not product.is_available:
            return jsonify({'msg': f'Product {product.name if product else "Unknown"} is not available'}), 400
        
        # Calculate price with any discounts
        price = product.price
        if product.discount_percentage > 0:
            price = price * (1 - (product.discount_percentage / 100))
        
        total += price * item.quantity
    
    # Generate order number (timestamp + user_id)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    order_number = f"{timestamp}-{user_id}"
    
    # Create order
    order = Order(
        user_id=user_id,
        order_number=order_number,
        total=total,
        status='pending',
        shipping_address=shipping_address,
        payment_method=payment_method
    )
    db.session.add(order)
    db.session.flush()  # Get order ID without committing
    
    # Create order items
    for item in cart_items:
        product = Product.query.get(item.product_id)
        
        # Calculate price with any discounts
        price = product.price
        if product.discount_percentage > 0:
            price = price * (1 - (product.discount_percentage / 100))
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=price
        )
        db.session.add(order_item)
    
    # Clear the cart
    CartItem.query.filter_by(cart_id=cart.id).delete()
    
    db.session.commit()
    
    return jsonify({
        'msg': 'Order created successfully',
        'order_id': order.id,
        'order_number': order_number
    }), 201

@order_bp.route('/<int:order_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    
    if not order:
        return jsonify({'msg': 'Order not found'}), 404
    
    # Only allow cancellation of pending orders
    if order.status != 'pending':
        return jsonify({'msg': f'Cannot cancel order with status: {order.status}'}), 400
    
    order.status = 'cancelled'
    db.session.commit()
    
    return jsonify({'msg': 'Order cancelled successfully'})
