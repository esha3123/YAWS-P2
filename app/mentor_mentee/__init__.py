from flask import Blueprint

mm_bp = Blueprint('mentor_mentee', __name__, url_prefix='/mentor-mentee')

from app.mentor_mentee.routes import mm_bp
