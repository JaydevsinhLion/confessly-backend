# ==========================================================
# 💬 CONFESSLY — FEEDBACK MODEL
# File: app/models/feedback.py
# Author: Jaydevsinh Gohil
# ==========================================================

from datetime import datetime
from app.db import get_db


class FeedbackModel:
    """Handles storing and retrieving user feedback."""

    @staticmethod
    def _collection():
        db = get_db()
        if not db:
            raise ConnectionError("Database not initialized. Call init_db() first.")
        return db.feedback

    @staticmethod
    def create_feedback(data):
        data["created_at"] = datetime.utcnow()
        FeedbackModel._collection().insert_one(data)

    @staticmethod
    def get_all():
        return list(FeedbackModel._collection().find().sort("created_at", -1))
