# ==========================================================
# 💬 CONFESSLY — REACTION MODEL
# File: app/models/reaction.py
# Author: Jaydevsinh Gohil
# ==========================================================

from datetime import datetime
from bson import ObjectId
from app.db import get_db


class ReactionModel:
    """Tracks emoji reactions for confessions."""

    @staticmethod
    def _collection():
        db = get_db()
        if not db:
            raise ConnectionError("Database not initialized. Call init_db() first.")
        return db.reactions

    @staticmethod
    def add_reaction(confession_id, emoji, session_id):
        ReactionModel._collection().update_one(
            {"confession_id": ObjectId(confession_id), "emoji": emoji},
            {
                "$inc": {"count": 1},
                "$addToSet": {"session_ids": session_id},
                "$set": {"created_at": datetime.utcnow()}
            },
            upsert=True
        )
