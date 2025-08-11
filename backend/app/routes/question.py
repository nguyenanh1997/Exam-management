from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Question, MonHoc
from app.routes.admin_required import admin_required

question_bp = Blueprint('question_bp', __name__, url_prefix='/api/questions')

# ✅ GET all questions
@question_bp.route('/', methods=['GET'])
@jwt_required()
def get_questions():
    questions = Question.query.all()
    return jsonify([{
        "id": q.id,
        "content": q.content,
        "difficulty": q.difficulty,
        "answer": q.correct_answer,
        "MonHoc_id": q.monhoc_id,
        "MonHoc_name": q.monhoc.name
    } for q in questions])

# ✅ POST new question — admin only
@question_bp.route('/', methods=['POST'])
@admin_required
def create_question():
    data = request.get_json()
    required_fields = ['content', 'answer', 'monhoc_id', "difficulty"]
    if not all(field in data for field in required_fields):
        return jsonify(msg="Missing fields"), 400

    MonHoc = MonHoc.query.get(data['monhoc_id'])
    if not MonHoc:
        return jsonify(msg="MonHoc not found"), 404

    if data['difficulty'] not in ['easy', 'medium', 'hard']:
        return jsonify(msg="MonHoc dificulty not in list"), 404
    question = Question(
        content=data['content'],
        answer=data['answer'],
        monhoc_id=data['monhoc_id'],
        difficulty=data['difficulty']
    )
    db.session.add(question)
    db.session.commit()
    return jsonify(msg="Question created successfully"), 201

# ✅ PUT update question — admin only
@question_bp.route('/<int:question_id>', methods=['PUT'])
@admin_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.get_json()

    for field in ['content', 'answer', 'monhoc_id', "difficulty"]:
        if field in data:
            setattr(question, field, data[field])

    if 'honHhc_id' in data:
        MonHoc = MonHoc.query.get(data['monhoc_id'])
        if not MonHoc:
            return jsonify(msg="MonHoc not found"), 404
        question.MonHoc_id = data['monhoc_id']

    db.session.commit()
    return jsonify(msg="Question updated successfully")

# ✅ DELETE question — admin only
@question_bp.route('/<int:question_id>', methods=['DELETE'])
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify(msg="Question deleted successfully")
