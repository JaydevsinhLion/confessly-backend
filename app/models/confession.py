# ==========================================================
# 💬 CONFESSLY — CONFESSION MODEL
# File: app/models/confession.py
# Author: Jaydevsinh Gohil
# ==========================================================

from datetime import datetime
from bson import ObjectId
from app.db import get_db


class ConfessionModel:
    """Handles CRUD operations for confessions."""

    @staticmethod
    def _collection():
        """Fetch collection only after DB is initialized."""
        db = get_db()
        if not db:
            raise ConnectionError("Database not initialized. Call init_db() first.")
        return db.confessions

    @staticmethod
    def create(data):
        data["created_at"] = datetime.utcnow()
        data["status"] = "active"
        data["reactions"] = {
            "heart": 0, "laugh": 0, "sad": 0, "angry": 0, "relate": 0
        }
        result = ConfessionModel._collection().insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    def get_all():
        return list(ConfessionModel._collection().find({"status": "active"}))

    @staticmethod
    def get_by_id(confession_id):
        return ConfessionModel._collection().find_one({"_id": ObjectId(confession_id)})

    @staticmethod
    def update_reactions(confession_id, emoji):
        field = f"reactions.{emoji}"
        ConfessionModel._collection().update_one(
            {"_id": ObjectId(confession_id)},
            {"$inc": {field: 1}}
        )

    @staticmethod
    def delete(confession_id):
        ConfessionModel._collection().update_one(
            {"_id": ObjectId(confession_id)},
            {"$set": {"status": "deleted"}}
        )
