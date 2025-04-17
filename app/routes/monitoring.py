from flask import Blueprint, jsonify, current_app, request
from sqlalchemy import text
from app import db
import os
import psutil
import time

monitoring_bp = Blueprint('monitoring', __name__, url_prefix='/api/monitoring')

@monitoring_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring systems.
    Returns basic health information about the application.
    """
    health_data = {
        'status': 'ok',
        'timestamp': time.time(),
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'environment': os.getenv('FLASK_ENV', 'development')
    }
    
    # Check database connection
    try:
        db.session.execute(text('SELECT 1'))
        health_data['database'] = 'connected'
    except Exception as e:
        health_data['database'] = 'error'
        health_data['database_error'] = str(e)
        health_data['status'] = 'degraded'
    
    return jsonify(health_data)

@monitoring_bp.route('/metrics', methods=['GET'])
def metrics():
    """
    Basic metrics endpoint for monitoring systems.
    Returns system metrics like CPU and memory usage.
    """
    if os.getenv('FLASK_ENV') == 'production' and not current_app.debug:
        # Only allow metrics in development or with proper authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header != f"Bearer {os.getenv('METRICS_API_KEY')}":
            return jsonify({'error': 'Unauthorized'}), 401
    
    # System metrics
    metrics_data = {
        'cpu': {
            'percent': psutil.cpu_percent(interval=0.1),
            'count': psutil.cpu_count()
        },
        'memory': {
            'total': psutil.virtual_memory().total,
            'available': psutil.virtual_memory().available,
            'percent': psutil.virtual_memory().percent
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'free': psutil.disk_usage('/').free,
            'percent': psutil.disk_usage('/').percent
        }
    }
    
    return jsonify(metrics_data)

@monitoring_bp.route('/readiness', methods=['GET'])
def readiness():
    """
    Readiness probe for Kubernetes or other orchestration systems.
    Checks if the application is ready to serve traffic.
    """
    ready = True
    status_code = 200
    
    # Check database connection
    try:
        db.session.execute(text('SELECT 1'))
        database_status = 'ok'
    except Exception as e:
        database_status = f'error: {str(e)}'
        ready = False
        status_code = 503  # Service Unavailable
    
    response = {
        'ready': ready,
        'database': database_status,
        'timestamp': time.time()
    }
    
    return jsonify(response), status_code
