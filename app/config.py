# ==========================================================
# 💬 CONFESSLY — CONFIGURATION SETTINGS
# File: app/config.py
# Author: Jaydevsinh Gohil
# ==========================================================

import os
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

class Config:
    # Flask Core Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "confessly_secret_key")
    JWT_SECRET = os.getenv("JWT_SECRET", "confessly_jwt_secret")

    # MongoDB Connection
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://test:123@mark1.finafzi.mongodb.net/?retryWrites=true&w=majority&appName=mark1"
    )

    # Debug Mode
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
