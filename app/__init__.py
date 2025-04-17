from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('FLASK_ENV', silent=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints here
    from .routes.auth import auth_bp
    from .routes.user import user_bp
    from .routes.dashboard import dashboard_bp
    from .routes.product import product_bp
    from .routes.transaction import transaction_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(admin_bp)

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

    return app
