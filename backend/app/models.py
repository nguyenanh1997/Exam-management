from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# bảng user admin
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'


class MonHoc(db.Model):
    __tablename__ = 'monhoc'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class MonHoc_User(db.Model):
    __tablename__ = 'monhoc_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    monhoc_id = db.Column(db.Integer, db.ForeignKey('monhoc.id'), nullable=False)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(521), unique=True, nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    answer = db.Column(db.String(512), nullable=False)  # 'admin' or 'user'

class Question_MonHoc(db.Model):
    __tablename__ = 'question_monhoc'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    monhoc_id = db.Column(db.Integer, db.ForeignKey('monhoc.id'), nullable=False)

class Exam(db.Model):
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('monhoc.id'), nullable=False)#
    time = db.Column(db.Integer, nullable=False)  # Lần làm bài thi thứ mấy
    
class Attempt(db.Model):
    __tablename__ = 'attempt'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    passed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, nullable=False)

class AttemptQuestion(db.Model):
    __tablename__ = 'attempt_question'
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    