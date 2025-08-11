from flask import Blueprint, request, jsonify
from app.models import db, User
from app.services.auth_service import hash_password, verify_password
from flask_jwt_extended import create_access_token
import re
auth_bp = Blueprint('auth', __name__)



BANNED_USERNAMES = {"admin", "manager", "hitler", "putin"}

def is_strong_password(password):
    # Ít nhất 8 ký tự, 1 chữ hoa, 1 chữ thường, 1 số, 1 ký tự đặc biệt
    pattern = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
    )
    return pattern.match(password)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or role not in ['admin', 'user']:
        return jsonify({'msg': 'Missing fields or invalid role'}), 400
    
        # Check username cấm
    if username in BANNED_USERNAMES:
        return jsonify({'error': 'Username is not allowed'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'User already exists'}), 409
        # Check mật khẩu mạnh
    if not is_strong_password(password):
        return jsonify({'error': 'Password must be at least 8 characters long and include uppercase, lowercase, number, and special character'}), 400
    user = User(
        username=username,
        password_hash=hash_password(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': 'User created'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')


    user = User.query.filter_by(username=username).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(
        identity =str(user.id),
        additional_claims = {
        'username': user.username,
        'role': user.role
        }
    )
    return jsonify({'access_token': access_token}), 200
