# ==========================================================
# 💬 CONFESSLY — ADMIN CONTROLLER (FINAL VERSION)
# File: app/controllers/admin_controller.py
# Author: Jaydevsinh Gohil (Master of Code)
# ==========================================================

import os
import jwt
from datetime import datetime, timedelta
from flask import jsonify, request
from werkzeug.security import check_password_hash
from bson import ObjectId
from app.models.admin import AdminModel
from app.db import get_db
from app.utils.auth import admin_required


# ==========================================================
# 🔧 HELPER FUNCTIONS
# ==========================================================
def success(message, data=None, code=200):
    """Unified JSON success response."""
    body = {"message": message}
    if data:
        body["data"] = data
    return jsonify(body), code


def error(message, code=400):
    """Unified JSON error response."""
    return jsonify({"error": message}), code


# ==========================================================
# 1️⃣ REGISTER ADMIN (INITIAL SETUP)
# ==========================================================
def register_admin():
    """
    Create the very first admin account.
    Recommended: Disable this route after initial setup.
    """
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return error("Missing required fields", 400)

    existing_admin = AdminModel.find_by_username(username)
    if existing_admin:
        return error("Admin already exists", 409)

    AdminModel.create_admin(username, email, password)
    return success(f"Admin '{username}' created successfully", code=201)


# ==========================================================
# 2️⃣ ADMIN LOGIN (JWT AUTH)
# ==========================================================
def admin_login():
    """
    Logs in admin and returns JWT token.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not (username and password):
        return error("Username and password required", 400)

    admin = AdminModel.find_by_username(username)
    if not admin or not check_password_hash(admin["password_hash"], password):
        return error("Invalid credentials", 401)

    # Update login time
    AdminModel.update_login_time(username)

    payload = {
        "username": username,
        "role": admin.get("role", "superadmin"),
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET", "confessly_jwt_secret"), algorithm="HS256")

    return success("Login successful", {
        "token": token,
        "admin": {
            "username": admin["username"],
            "email": admin["email"],
            "role": admin["role"]
        }
    })


# ==========================================================
# 3️⃣ ADMIN PROFILE INFO
# ==========================================================
@admin_required
def get_admin_profile():
    """Returns the logged-in admin’s profile details."""
    decoded_admin = request.admin_user
    username = decoded_admin.get("username")
    admin = AdminModel.find_by_username(username)
    if not admin:
        return error("Admin not found", 404)

    return success("Admin profile fetched", {
        "username": admin["username"],
        "email": admin["email"],
        "role": admin["role"],
        "last_login": admin.get("last_login"),
        "created_at": admin.get("created_at")
    })


# ==========================================================
# 4️⃣ DASHBOARD SUMMARY DATA
# ==========================================================
@admin_required
def dashboard_summary():
    """Returns summary stats and recent confessions."""
    db = get_db()

    total_confessions = db.confessions.count_documents({})
    total_feedback = db.feedback.count_documents({})
    total_reports = db.reports.count_documents({}) if "reports" in db.list_collection_names() else 0
    total_users = db.sessions.count_documents({})

    recent_confessions = list(db.confessions.find().sort("created_at", -1).limit(5))
    for confession in recent_confessions:
        confession["_id"] = str(confession["_id"])
        confession.pop("ip_hash", None)

    return success("Dashboard summary fetched", {
        "stats": {
            "confessions": total_confessions,
            "feedback": total_feedback,
            "reports": total_reports,
            "users": total_users
        },
        "recent_confessions": recent_confessions
    })


# ==========================================================
# 5️⃣ VIEW FEEDBACK
# ==========================================================
@admin_required
def view_feedback():
    """Returns all feedback messages (sorted newest first)."""
    db = get_db()
    feedbacks = list(db.feedback.find().sort("created_at", -1))
    for f in feedbacks:
        f["_id"] = str(f["_id"])
    return success("Feedback fetched successfully", feedbacks)


# ==========================================================
# 6️⃣ DELETE CONFESSION (MODERATION)
# ==========================================================
@admin_required
def delete_confession(confession_id):
    """Marks a confession as deleted."""
    db = get_db()
    try:
        result = db.confessions.update_one(
            {"_id": ObjectId(confession_id)},
            {"$set": {"status": "deleted"}}
        )
        if result.modified_count == 0:
            return error("Confession not found", 404)
        return success("Confession deleted successfully")
    except Exception as e:
        return error(f"Invalid confession ID: {e}", 400)


# ==========================================================
# 7️⃣ VIEW ALL REPORTS
# ==========================================================
@admin_required
def view_reports():
    """Shows all user-submitted reports."""
    db = get_db()
    if "reports" not in db.list_collection_names():
        return success("No reports found", [])

    reports = list(db.reports.find().sort("created_at", -1))
    for r in reports:
        r["_id"] = str(r["_id"])
    return success("Reports fetched successfully", reports)


# ==========================================================
# 8️⃣ SYSTEM HEALTH CHECK
# ==========================================================
@admin_required
def system_health():
    """Returns system status & DB stats for monitoring."""
    db = get_db()
    try:
        db_stats = db.command("dbStats")
        print(f"🔍 Health check at {datetime.utcnow()} | DB size: {db_stats['dataSize']} bytes")
        return success("System healthy", {
            "database_size_MB": round(db_stats["dataSize"] / 1024 / 1024, 2),
            "collections": db.list_collection_names(),
            "server_time": datetime.utcnow().isoformat() + "Z"
        })
    except Exception as e:
        return error(f"Health check failed: {str(e)}", 500)


# ==========================================================
# 9️⃣ LIST ALL ADMINS
# ==========================================================
@admin_required
def get_all_admins():
    """Returns list of all admins (for superadmin only)."""
    decoded = request.admin_user
    if decoded.get("role") != "superadmin":
        return error("Unauthorized access", 403)

    db = get_db()
    admins = list(db.admins.find({}, {"password_hash": 0}))
    for a in admins:
        a["_id"] = str(a["_id"])
    return success("All admins fetched", admins)


# ==========================================================
# 🔟 CREATE NEW MODERATOR (By Superadmin)
# ==========================================================
@admin_required
def create_moderator():
    """Allows superadmin to create a new moderator."""
    decoded = request.admin_user
    if decoded.get("role") != "superadmin":
        return error("Only superadmins can create moderators", 403)

    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return error("Missing fields", 400)

    existing = AdminModel.find_by_username(username)
    if existing:
        return error("Username already exists", 409)

    AdminModel.create_admin(username, email, password, role="moderator")
    return success(f"Moderator '{username}' created successfully", code=201)


# ==========================================================
# 11️⃣ DELETE ADMIN (Superadmin Only)
# ==========================================================
@admin_required
def delete_admin(username):
    """Deletes another admin (superadmin only)."""
    decoded = request.admin_user
    if decoded.get("role") != "superadmin":
        return error("Only superadmins can delete admins", 403)

    db = get_db()
    result = db.admins.delete_one({"username": username})
    if result.deleted_count == 0:
        return error("Admin not found", 404)
    return success(f"Admin '{username}' deleted")


# ==========================================================
# 12️⃣ SEARCH CONFESSIONS BY MOOD / STATUS
# ==========================================================
@admin_required
def search_confessions():
    """Allows admin to search confessions by mood or status."""
    db = get_db()
    mood = request.args.get("mood")
    status = request.args.get("status", "active")

    query = {}
    if mood:
        query["mood"] = mood
    if status:
        query["status"] = status

    confessions = list(db.confessions.find(query).sort("created_at", -1))
    for c in confessions:
        c["_id"] = str(c["_id"])
    return success("Confessions search results", confessions)
