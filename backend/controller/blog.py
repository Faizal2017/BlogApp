from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.blog_model import create_blog, get_all_blogs, get_blog_by_id, update_blog, delete_blog

blog_bp = Blueprint("blogs", __name__)

@blog_bp.route("/", methods=["GET"])
def all_blogs():
    db = current_app.db
    blogs = get_all_blogs(db)
    for blog in blogs:
        blog["_id"] = str(blog["_id"])
        blog["created_at"] = blog["created_at"].isoformat()
    return jsonify(blogs), 200

@blog_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    db = current_app.db
    data = request.get_json()
    user_id = get_jwt_identity()
    author = user_id  # storing author as user ID

    if not data.get("title") or not data.get("content"):
        return jsonify({"message": "Missing fields"}), 400

    blog = create_blog(db, data["title"], data["content"], author)
    blog["_id"] = str(blog["_id"])
    blog["created_at"] = blog["created_at"].isoformat()
    return jsonify(blog), 201

@blog_bp.route("/<blog_id>", methods=["GET"])
def get_one(blog_id):
    db = current_app.db
    blog = get_blog_by_id(db, blog_id)
    if not blog:
        return jsonify({"message": "Blog not found"}), 404
    blog["_id"] = str(blog["_id"])
    blog["created_at"] = blog["created_at"].isoformat()
    return jsonify(blog), 200

@blog_bp.route("/<blog_id>", methods=["PUT"])
@jwt_required()
def update(blog_id):
    db = current_app.db
    data = request.get_json()
    updated_blog = update_blog(db, blog_id, data.get("title"), data.get("content"))
    if not updated_blog:
        return jsonify({"message": "Blog not found"}), 404
    updated_blog["_id"] = str(updated_blog["_id"])
    updated_blog["created_at"] = updated_blog["created_at"].isoformat()
    return jsonify(updated_blog), 200

@blog_bp.route("/<blog_id>", methods=["DELETE"])
@jwt_required()
def delete(blog_id):
    db = current_app.db
    result = delete_blog(db, blog_id)
    if result.deleted_count == 0:
        return jsonify({"message": "Blog not found"}), 404
    return jsonify({"message": "Deleted successfully"}), 200
