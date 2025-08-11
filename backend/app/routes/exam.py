import random
from sqlalchemy import and_
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Question, Question_MonHoc, Attempt, AttemptQuestion

exam_bp = Blueprint("exam_bp", __name__, url_prefix="/api/exam")

@exam_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_exam():
    user_id = get_jwt_identity()
    data = request.json
    monhoc_id = data.get("monhoc_id")

    # Lấy tất cả câu hỏi đã làm đúng từ trước
    correct_q_ids = db.session.query(AttemptQuestion.question_id).join(Attempt).filter(
        Attempt.user_id == user_id,
        AttemptQuestion.is_correct == True
    ).distinct().all()

    correct_q_ids = [q[0] for q in correct_q_ids]

    # Lấy danh sách câu hỏi theo mức độ, loại trừ những câu đã làm đúng
    def get_questions(level, count):
        return db.session.query(Question).join(Question_MonHoc).filter(
            Question.difficulty == level,
            Question_MonHoc.monhoc_id == monhoc_id,
            ~Question.id.in_(correct_q_ids)
        ).order_by(db.func.random()).limit(count).all()

    easy_qs = get_questions("easy", 5)
    medium_qs = get_questions("medium", 3)
    hard_qs = get_questions("hard", 2)
    # very_hard_qs = get_questions("very_hard", 2)

    selected_questions = easy_qs + medium_qs + hard_qs # + very_hard_qs

    if len(selected_questions) < 10:
        return jsonify(msg="Không đủ câu hỏi chưa làm đúng, Bạn đã thất bại"), 400

    # Tạo exam tạm thời (nếu muốn), trả về danh sách câu hỏi
    return jsonify({
        "questions": [{
            "id": q.id,
            "content": q.content
        } for q in selected_questions]
    })


@exam_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_exam():
    user_id = get_jwt_identity()
    data = request.json

    questions = data.get("questions")  # [{"id": 1, "answer": "A"}, ...]
    if not questions:
        return jsonify(msg="No answers submitted"), 400

    correct = 0
    attempt = Attempt(user_id=user_id, exam_id=0, passed=False, score=0)
    db.session.add(attempt)
    db.session.commit()

    for item in questions:
        q = Question.query.get(item["id"])
        is_correct = (q.answer == item["answer"])
        if is_correct:
            correct += 1

        db.session.add(AttemptQuestion(
            attempt_id=attempt.id,
            question_id=q.id,
            is_correct=is_correct
        ))

    passed = correct >= 8
    attempt.passed = passed
    attempt.score = correct
    db.session.commit()

    return jsonify(msg="Exam submitted", passed=passed, score=correct)
