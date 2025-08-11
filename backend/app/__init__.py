from flask import Flask
from app.models import db
from flask_jwt_extended import JWTManager
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.routes.subject import subject_bp
from app.routes.exam import exam_bp
from app.routes.question import question_bp
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['DEBUG'] = True
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp)
    app.register_blueprint(subject_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(exam_bp)

    api = Api(app, version="1.0", title="My Flask API",
          description="API documentation with Swagger (Flask-RESTX)",
          doc='/docs')  # Swagger UI available at /docs

    return app
