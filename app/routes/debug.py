from flask import Blueprint, jsonify
from ..models.user import User

debug_bp = Blueprint('debug', __name__)

# /api/debug
@debug_bp.route('/api/debug', methods=['GET'])
def api_debug():
    return jsonify({'msg': 'API Debug Endpoint'}), 200

# /debug/health and /api/debug/health
@debug_bp.route('/debug/health', methods=['GET'])
def debug_health():
    return jsonify({'status': 'ok', 'env': 'debug'}), 200

@debug_bp.route('/api/debug/health', methods=['GET'])
def api_debug_health():
    return jsonify({'status': 'ok', 'env': 'api-debug'}), 200

# /debug/users and /api/debug/users
@debug_bp.route('/debug/users', methods=['GET'])
def debug_users():
    users = User.query.all()
    return jsonify({'users': [u.email for u in users]}), 200

@debug_bp.route('/api/debug/users', methods=['GET'])
def api_debug_users():
    users = User.query.all()
    return jsonify({'users': [u.email for u in users]}), 200

# /debug/status and /api/debug/status
@debug_bp.route('/debug/status', methods=['GET'])
def debug_status():
    return jsonify({'status': 'debug', 'uptime': 'unknown'}), 200

@debug_bp.route('/api/debug/status', methods=['GET'])
def api_debug_status():
    return jsonify({'status': 'api-debug', 'uptime': 'unknown'}), 200

# /debug/info and /api/debug/info
@debug_bp.route('/debug/info', methods=['GET'])
def debug_info():
    return jsonify({'info': 'Debug Info', 'env': 'debug'}), 200

@debug_bp.route('/api/debug/info', methods=['GET'])
def api_debug_info():
    return jsonify({'info': 'API Debug Info', 'env': 'api-debug'}), 200

# /dev
@debug_bp.route('/dev', methods=['GET'])
def dev():
    return jsonify({'msg': 'Dev Endpoint'}), 200

# /dev/info
@debug_bp.route('/dev/info', methods=['GET'])
def dev_info():
    return jsonify({'info': 'Dev Info'}), 200

# /dev/health
@debug_bp.route('/dev/health', methods=['GET'])
def dev_health():
    return jsonify({'status': 'ok', 'env': 'dev'}), 200

# /test
@debug_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'msg': 'Test Endpoint'}), 200

# /test/health
@debug_bp.route('/test/health', methods=['GET'])
def test_health():
    return jsonify({'status': 'ok', 'env': 'test'}), 200

# /test/users
@debug_bp.route('/test/users', methods=['GET'])
def test_users():
    users = User.query.all()
    return jsonify({'users': [u.email for u in users]}), 200

# /admin/debug
@debug_bp.route('/admin/debug', methods=['GET'])
def admin_debug():
    return jsonify({'msg': 'Admin Debug Endpoint'}), 200

# /admin/info
@debug_bp.route('/admin/info', methods=['GET'])
def admin_info():
    return jsonify({'info': 'Admin Info'}), 200

# /admin/users
@debug_bp.route('/admin/users', methods=['GET'])
def admin_users():
    users = User.query.all()
    return jsonify({'users': [u.email for u in users]}), 200
