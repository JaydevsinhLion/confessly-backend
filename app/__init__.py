# ==========================================================
# 💬 CONFESSLY — APP INITIALIZER
# File: app/__init__.py
# Author: Jaydevsinh Gohil
# ==========================================================

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .db import init_db
from .routes.admin_routes import admin_bp


def create_app():
    """Main Flask application factory."""
    load_dotenv()  # Load .env file
    app = Flask(__name__)

    # Enable CORS for all domains (optional: restrict in prod)
    CORS(app)

    # Initialize MongoDB
    init_db(app)

    # Register Blueprints
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # Root route (for quick API health check)
    @app.route("/")
    def home():
        return {"message": "💬 Confessly API running successfully"}

    return app
