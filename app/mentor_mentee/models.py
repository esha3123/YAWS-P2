from app.models.models import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# User table (Base for all - admin, mentor, mentee)
class MentorMenteeUser(db.Model):
    __tablename__ = 'mentor_mentee_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'mentor', 'mentee'
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Mentor Profile
class MentorProfile(db.Model):
    __tablename__ = 'mentor_profile'
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor_mentee_user.id'), unique=True)
    department = db.Column(db.String(80))
    subject = db.Column(db.String(120))
    bio = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Mentee Profile
class MenteeProfile(db.Model):
    __tablename__ = 'mentee_profile'
    id = db.Column(db.Integer, primary_key=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentor_mentee_user.id'), unique=True)
    department = db.Column(db.String(80))
    year = db.Column(db.Integer)
    roll_no = db.Column(db.String(40))
    assigned_mentor_id = db.Column(db.Integer, db.ForeignKey('mentor_mentee_user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Monthly Form (Mentee submits, Mentor reviews)
class MenteeMonthlyForm(db.Model):
    __tablename__ = 'mentee_monthly_form'
    id = db.Column(db.Integer, primary_key=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentor_mentee_user.id'), nullable=False)
    month_year = db.Column(db.String(20), nullable=False)  # "Jan 2026"
    learning_progress = db.Column(db.Text)
    challenges = db.Column(db.Text)
    goals_this_month = db.Column(db.Text)
    mentor_feedback = db.Column(db.Text)
    mentor_rating = db.Column(db.Integer)  # 1-5
    status = db.Column(db.String(20), default='submitted')  # submitted, reviewed
    submitted_date = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_date = db.Column(db.DateTime)

# Yearly Form (Mentee submits, Mentor reviews)
class MenteeYearlyForm(db.Model):
    __tablename__ = 'mentee_yearly_form'
    id = db.Column(db.Integer, primary_key=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentor_mentee_user.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    summary_of_progress = db.Column(db.Text)
    achievements = db.Column(db.Text)
    challenges_over_year = db.Column(db.Text)
    mentor_feedback = db.Column(db.Text)
    mentor_rating = db.Column(db.Integer)
    status = db.Column(db.String(20), default='submitted')  # submitted, reviewed
    submitted_date = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_date = db.Column(db.DateTime)
