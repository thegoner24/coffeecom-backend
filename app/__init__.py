from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
import time

# Import our database adapter for psycopg2cffi compatibility
from app.database import *

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Handle proxy servers in production
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Load configuration
    if test_config is None:
        app.config.from_envvar('FLASK_ENV', silent=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2592000  # 30 days
        
        # Production settings
        if os.getenv('FLASK_ENV') == 'production':
            app.config['SESSION_COOKIE_SECURE'] = True
            app.config['SESSION_COOKIE_HTTPONLY'] = True
            app.config['REMEMBER_COOKIE_SECURE'] = True
            app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    else:
        # For testing
        app.config.update(test_config)
    
    # Set up extensions with custom engine configuration for psycopg2cffi compatibility
    if app.config.get('SQLALCHEMY_DATABASE_URI'):
        # Use a custom engine configuration for PostgreSQL
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql'):
            app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                'connect_args': {'connect_timeout': 10},
                'pool_pre_ping': True,
                'pool_recycle': 300,
            }
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Set up CORS for ALL origins for all API endpoints (OPEN for frontend use)
    # NOTE: For production, restrict 'origins' to your frontend domain(s) only!
    CORS(app, resources={r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True
    }})
    
    # Set up rate limiting
    limiter.init_app(app)
    
    # Set up logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/coffeecom.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('CoffeeCom startup')
    
    # Request timing middleware
    @app.before_request
    def before_request():
        request.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Log request timing
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            app.logger.info(f"Request to {request.path} took {duration:.2f}s")
        
        return response
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Not found'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500

    # Register blueprints here
    from .routes.auth import auth_bp
    from .routes.user import user_bp
    from .routes.dashboard import dashboard_bp
    from .routes.product import product_bp
    from .routes.transaction import transaction_bp
    from .routes.admin import admin_bp
    from .routes.monitoring import monitoring_bp
    from .routes.cart import cart_bp
    from .routes.order import order_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(monitoring_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)

    # Serve index.html at root
    @app.route("/")
    def index():
        return render_template("index.html")

    # Serve login.html at /login
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            # This is a frontend template only; backend login logic is via API
            return redirect(url_for("dashboard"))
        return render_template("login.html")

    # Serve register.html at /register
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            return redirect(url_for("login"))
        return render_template("register.html")

    # Serve dashboard.html at /dashboard
    @app.route("/dashboard")
    def dashboard():
        # In a real app, fetch stats for the user here
        return render_template("dashboard.html")

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'ok'}), 200

    return app
