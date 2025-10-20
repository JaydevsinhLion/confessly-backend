# ==========================================================
# 💬 CONFESSLY — ADMIN MODEL
# File: app/models/admin.py
# Author: Jaydevsinh Gohil
# ==========================================================

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db


class AdminModel:
    """Handles admin creation, authentication, and management."""

    @staticmethod
    def _collection():
        """Fetch the admins collection only after DB initialization."""
        db = get_db()
        if not db:
            raise ConnectionError("Database not initialized. Call init_db() first.")
        return db.admins

    # ------------------------------------------------------
    # Create new admin
    # ------------------------------------------------------
    @staticmethod
    def create_admin(username, email, password, role="superadmin"):
        hashed_pw = generate_password_hash(password)
        admin = {
            "username": username,
            "email": email,
            "password_hash": hashed_pw,
            "role": role,
            "permissions": ["view_analytics", "manage_users", "delete_confession"],
            "status": "active",
            "created_at": datetime.utcnow(),
            "last_login": None
        }
        AdminModel._collection().insert_one(admin)

    # ------------------------------------------------------
    # Find admin by username
    # ------------------------------------------------------
    @staticmethod
    def find_by_username(username):
        return AdminModel._collection().find_one({"username": username})

    # ------------------------------------------------------
    # Verify password
    # ------------------------------------------------------
    @staticmethod
    def verify_password(admin_data, password):
        return check_password_hash(admin_data["password_hash"], password)

    # ------------------------------------------------------
    # Update last login timestamp
    # ------------------------------------------------------
    @staticmethod
    def update_login_time(username):
        AdminModel._collection().update_one(
            {"username": username},
            {"$set": {"last_login": datetime.utcnow()}}
        )
