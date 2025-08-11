from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models import User
from app import db
from app.routes.admin_required import admin_required  # middleware từ bước 2

admin_bp = Blueprint('admin_bp', __name__, url_prefix="/api/admin")

@admin_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "role": u.role
    } for u in users])

@admin_bp.route('/', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify(msg="Username already exists"), 400

    user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        role=data.get('role', 'user')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(msg="User created successfully")

@admin_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    user.username = data.get('username', user.username)
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    if 'role' in data:
        user.role = data['role']

    db.session.commit()
    return jsonify(msg="User updated successfully")

@admin_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(msg="User deleted successfully")
