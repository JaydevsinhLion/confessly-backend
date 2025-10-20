# ==========================================================
# 💬 CONFESSLY — DATABASE CONFIGURATION
# File: app/db.py
# Author: Jaydevsinh Gohil
# ==========================================================

from pymongo import MongoClient
import os

client = None
db = None


def init_db(app):
    """Initialize MongoDB connection and create TTL indexes."""
    global client, db

    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("⚠️ MONGO_URI not found in environment variables.")

    # TLS fix for GitHub Codespaces + MongoDB Atlas SSL handshake issue
    client = MongoClient(
        mongo_uri,
        tls=True,
        tlsAllowInvalidCertificates=True,  # remove this in production if you have valid CA certs
        serverSelectionTimeoutMS=20000
    )

    db = client.get_database("confessly")

    # Create TTL indexes (auto-delete old data)
    try:
        db.confessions.create_index("created_at", expireAfterSeconds=86400)   # 24 hrs
        db.replies.create_index("created_at", expireAfterSeconds=86400)
        db.sessions.create_index("last_activity", expireAfterSeconds=604800)  # 7 days
        print("✅ MongoDB connected and TTL indexes applied!")
    except Exception as e:
        print(f"⚠️ MongoDB index creation skipped or failed: {e}")

    # Attach DB to app context
    app.db = db


def get_db():
    """Returns current MongoDB instance."""
    return db
