# ==========================================================
# 💬 CONFESSLY — SESSION MODEL
# File: app/models/session.py
# Author: Jaydevsinh Gohil
# ==========================================================

from datetime import datetime
from uuid import uuid4
from app.db import get_db


class SessionModel:
    """Stores temporary user sessions for analytics."""

    @staticmethod
    def _collection():
        db = get_db()
        if not db:
            raise ConnectionError("Database not initialized. Call init_db() first.")
        return db.sessions

    @staticmethod
    def create():
        session = {
            "session_id": str(uuid4()),
            "confession_count": 0,
            "mood_profile": {},
            "last_activity": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
        SessionModel._collection().insert_one(session)
        return session["session_id"]

    @staticmethod
    def update_activity(session_id):
        SessionModel._collection().update_one(
            {"session_id": session_id},
            {"$set": {"last_activity": datetime.utcnow()}}
        )
