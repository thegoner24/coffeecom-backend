from flask import Blueprint, request, jsonify
from .. import db
from ..models.transaction import Transaction
from flask_jwt_extended import jwt_required, get_jwt_identity

transaction_bp = Blueprint('transaction', __name__, url_prefix='/api/transactions')

@transaction_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'id': t.id,
            'order_id': t.order_id,
            'user_id': t.user_id,
            'amount': t.amount,
            'status': t.status,
            'payment_method': t.payment_method,
            'payment_id': t.payment_id,
            'created_at': t.created_at,
            'updated_at': t.updated_at
        } for t in transactions
    ])

@transaction_bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return jsonify({'msg': 'Transaction not found'}), 404
    return jsonify({
        'id': transaction.id,
        'order_id': transaction.order_id,
        'user_id': transaction.user_id,
        'amount': transaction.amount,
        'status': transaction.status,
        'payment_method': transaction.payment_method,
        'payment_id': transaction.payment_id,
        'created_at': transaction.created_at,
        'updated_at': transaction.updated_at
    })

@transaction_bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()
    transaction = Transaction(
        order_id=data['order_id'],
        user_id=user_id,
        amount=data['amount'],
        status=data.get('status', 'pending'),
        payment_method=data.get('payment_method'),
        payment_id=data.get('payment_id')
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'msg': 'Transaction created', 'id': transaction.id}), 201
