from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import MonHoc, MonHoc_User
from app import db
from app.routes.admin_required import admin_required

subject_bp = Blueprint('subject_bp', __name__, url_prefix="/api/monhoc")

# ✅ GET all subjects — ai có token cũng xem được
@subject_bp.route('', methods=['GET'])
@jwt_required()
def get_subjects():
    try:
        subjects = MonHoc.query.all()
        return jsonify([{
            "id": s.id,
            "name": s.name,
        } for s in subjects])
    except Exception as e:
        return jsonify(msg="Error fetching subjects", error=str(e)), 500

# ✅ POST new subject — chỉ admin
@subject_bp.route('', methods=['POST'])
@admin_required
def create_subject():
    try:#
        data = request.get_json()
        if not data.get('name'):
            return jsonify(msg=f"Subject name is required"), 400
        if MonHoc.query.filter_by(name=data['name']).first():
            return jsonify(msg=f"Subject {data['name']} exists"), 400
        
        subject = MonHoc(name=data['name'])
        db.session.add(subject)
        db.session.commit()
        return jsonify(msg=f"Subject created successfully: {subject.id}"), 201
    except Exception as e:
        return jsonify(msg="Error create subjects", error=str(e)), 500

# ✅ PUT update subject — chỉ admin
@subject_bp.route('/<int:subject_id>', methods=['PUT'])
@admin_required
def update_subject(subject_id):
    try:
        subject = MonHoc.query.get_or_404(subject_id)
        data = request.get_json()
        if 'name' in data:
            subject.name = data['name']

        db.session.commit()
        return jsonify(msg=f"Subject updated successfully id: {subject.id}")

    except Exception as e:
        return jsonify(msg="Error update subjects", error=str(e)), 500
 

# ✅ DELETE subject — chỉ admin
@subject_bp.route('/<int:subject_id>', methods=['DELETE'])
@admin_required
def delete_subject(subject_id):
    try:
        subject = MonHoc.query.get_or_404(subject_id)
        db.session.delete(subject)
        db.session.commit()
        return jsonify(msg=f"Subject deleted successfully id: {subject.id}")
    except Exception as e:
        return jsonify(msg="Error deleting subject", error=str(e)), 500


@subject_bp.route('/<int:subject_id>/assign', methods=['POST'])
@admin_required
def assign_subject_to_user(subject_id):
    try:
        subject = MonHoc.query.get_or_404(subject_id)
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        for user_id in user_ids:
            # ở đây tồn tại lỗi không kiểm tra user_id có tồn tại trong bảng User hay không
            # không kiểm tra user đó có phải role user hay không? 
            if not MonHoc_User.query.filter_by(user_id=user_id, monhoc_id=subject.id).first():
                new_assignment = MonHoc_User(user_id=user_id, monhoc_id=subject.id)
                db.session.add(new_assignment)
        db.session.commit()
    except Exception as e:
        return jsonify(msg="Error assigning subject to user", error=str(e)), 500
    
@subject_bp.route('/<int:user_id>/getsubjects', methods=['GET'])
@jwt_required()
def get_subjects_by_user(user_id):
    # tại chức năng này tồn tại lỗi không kiểm tra user_id có tồn tại trong bảng User hay không
    # tại chức năng này không kiểm tra mã jwt có phải là của user đó hay không
    try:
        subjects = MonHoc.query.join(MonHoc_User).filter(MonHoc_User.user_id == user_id).all()
        return jsonify([{
            "id": s.id,
            "name": s.subject_name,
        } for s in subjects])
    except Exception as e:
        return jsonify(msg="Error fetching subjects for user", error=str(e)), 500