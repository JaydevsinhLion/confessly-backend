# ==========================================================
# 💬 CONFESSLY — USER MODEL
# File: app/models/user.py
# Author: Jaydevsinh Gohil
# ==========================================================

from datetime import datetime
from uuid import uuid4
from app.db import get_db


class UserModel:
    """Handles creation and tracking of guest or registered users."""

    @staticmethod
    def _collection():
        """Fetch users collection after DB initialization."""
        db = get_db()
        if not db:
            raise ConnectionError("Database not initialized. Call init_db() first.")
        return db.users

    @staticmethod
    def create_guest():
        """Create a guest user session."""
        user = {
            "session_id": str(uuid4()),
            "type": "guest",
            "email": None,
            "username": None,
            "confessions": [],
            "replies": [],
            "mood_profile": {},
            "last_active": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
        result = UserModel._collection().insert_one(user)
        return str(result.inserted_id)

    @staticmethod
    def find_by_session(session_id):
        """Find user by their session ID."""
        return UserModel._collection().find_one({"session_id": session_id})

    @staticmethod
    def update_activity(session_id):
        """Update last active timestamp."""
        UserModel._collection().update_one(
            {"session_id": session_id},
            {"$set": {"last_active": datetime.utcnow()}}
        )

    @staticmethod
    def add_confession(session_id, confession_id):
        """Link a confession to a user session."""
        UserModel._collection().update_one(
            {"session_id": session_id},
            {"$push": {"confessions": confession_id}}
        )
