# ==========================================================
# 💬 CONFESSLY — ADMIN ROUTES (Blueprint)
# File: app/routes/admin_routes.py
# Author: Jaydevsinh Gohil
# ==========================================================

from flask import Blueprint
from app.controllers.admin_controller import (
    register_admin,
    admin_login,
    get_admin_profile,
    dashboard_summary,
    view_feedback,
    delete_confession,
    view_reports,
    system_health,
    get_all_admins,
    create_moderator,
    delete_admin,
    search_confessions
)

# ----------------------------------------------------------
# Blueprint Initialization
# ----------------------------------------------------------
admin_bp = Blueprint("admin", __name__)

# ----------------------------------------------------------
# Public Routes (No Auth Required)
# ----------------------------------------------------------
admin_bp.route("/register", methods=["POST"])(register_admin)
admin_bp.route("/login", methods=["POST"])(admin_login)

# ----------------------------------------------------------
# Protected Routes (JWT Required)
# ----------------------------------------------------------
admin_bp.route("/profile", methods=["GET"])(get_admin_profile)
admin_bp.route("/dashboard", methods=["GET"])(dashboard_summary)
admin_bp.route("/feedback", methods=["GET"])(view_feedback)
admin_bp.route("/confessions/<string:confession_id>", methods=["DELETE"])(delete_confession)
admin_bp.route("/reports", methods=["GET"])(view_reports)
admin_bp.route("/health", methods=["GET"])(system_health)
admin_bp.route("/all", methods=["GET"])(get_all_admins)
admin_bp.route("/moderator", methods=["POST"])(create_moderator)
admin_bp.route("/delete/<string:username>", methods=["DELETE"])(delete_admin)
admin_bp.route("/search", methods=["GET"])(search_confessions)
