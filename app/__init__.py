from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
import os
from app.config.config import config
from app.models.models import db
from app.mentor_mentee.models import (
    MentorMenteeUser, MenteeProfile, MentorProfile,
    MenteeMonthlyForm, MenteeYearlyForm
)

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    CORS(app)
    Migrate(app, db)
    
    with app.app_context():
        db.create_all()
    
    from app.api import api_bp
    from app.auth import auth_bp
    from app.frontend import frontend_bp
    from app.mentor_mentee.routes import mm_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp)
    app.register_blueprint(frontend_bp)
    app.register_blueprint(mm_bp, url_prefix='/mentor-mentee')
    
    @app.route('/uploads/<path:filename>')
    def custom_static(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    return app
