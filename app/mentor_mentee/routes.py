from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from app.mentor_mentee.models import (
    MentorMenteeUser, MenteeProfile, MentorProfile, 
    MenteeMonthlyForm, MenteeYearlyForm
)
from app import db
import csv
import io
from datetime import timedelta

mm_bp = Blueprint('mentor_mentee', __name__, url_prefix='/mentor-mentee')

@mm_bp.before_request
def before_request():
    """Make sessions permanent"""
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(days=7)

# ==================== ADMIN ROUTES ====================

@mm_bp.route('/admin/upload-roles', methods=['GET', 'POST'])
def admin_upload_roles():
    """Admin uploads role CSV (first time setup + yearly updates)"""
    # Check if admin is logged in
    if session.get('user_role') != 'admin':
        flash('Admin access only', 'error')
        return redirect(url_for('mentor_mentee.login'))
    
    if request.method == 'POST':
        file = request.files.get('csv_file')
        if not file:
            flash('No file uploaded', 'error')
            return redirect(url_for('mentor_mentee.admin_upload_roles'))
        
        try:
            stream = io.StringIO(file.stream.read().decode('utf-8'))
            reader = csv.DictReader(stream)
            count_added = 0
            count_updated = 0
            
            for row in reader:
                email = row.get('email', '').strip()
                name = row.get('name', '').strip()
                role = row.get('role', '').strip()
                
                if not email or not name or not role:
                    continue
                
                user = MentorMenteeUser.query.filter_by(email=email).first()
                
                if user:
                    # Update existing user
                    user.name = name
                    user.role = role
                    count_updated += 1
                else:
                    # Add new user
                    user = MentorMenteeUser(
                        email=email,
                        name=name,
                        role=role,
                        verified=False
                    )
                    db.session.add(user)
                    db.session.flush()
                    count_added += 1
                    
                    # Add profile if mentee or mentor
                    if role == 'mentee':
                        profile = MenteeProfile(
                            mentee_id=user.id,
                            department=row.get('department', ''),
                            year=int(row.get('year', 0)) if row.get('year') else None,
                            roll_no=row.get('roll_no', '')
                        )
                        db.session.add(profile)
                    elif role == 'mentor':
                        profile = MentorProfile(
                            mentor_id=user.id,
                            department=row.get('department', ''),
                            subject=row.get('subject', ''),
                            bio=row.get('bio', '')
                        )
                        db.session.add(profile)
            
            db.session.commit()
            flash(f'Roles uploaded! Added: {count_added}, Updated: {count_updated}', 'success')
            return redirect(url_for('mentor_mentee.admin_dashboard'))
        
        except Exception as e:
            current_app.logger.error(f"Error uploading roles: {str(e)}")
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('mentor_mentee.admin_upload_roles'))
    
    return render_template('mentor_mentee/admin_upload_roles.html')

@mm_bp.route('/admin/dashboard')
def admin_dashboard():
    """Admin sees all mentees, mentors, and forms"""
    if session.get('user_role') != 'admin':
        flash('Admin access only', 'error')
        return redirect(url_for('mentor_mentee.login'))
    
    all_mentees = MenteeProfile.query.all()
    all_mentors = MentorProfile.query.all()
    all_monthly_forms = MenteeMonthlyForm.query.all()
    all_yearly_forms = MenteeYearlyForm.query.all()
    
    return render_template('mentor_mentee/admin_dashboard.html',
                          mentees=all_mentees,
                          mentors=all_mentors,
                          monthly_forms=all_monthly_forms,
                          yearly_forms=all_yearly_forms)

# ==================== MENTOR ROUTES ====================

@mm_bp.route('/mentor/upload-mentees', methods=['GET', 'POST'])
def mentor_upload_mentees():
    """Mentor uploads CSV of their assigned mentees"""
    if session.get('user_role') != 'mentor':
        flash('Mentor access only', 'error')
        return redirect(url_for('mentor_mentee.login'))
    
    mentor_id = session.get('user_id')
    
    if request.method == 'POST':
        file = request.files.get('csv_file')
        if not file:
            flash('No file uploaded', 'error')
            return redirect(url_for('mentor_mentee.mentor_upload_mentees'))
        
        try:
            stream = io.StringIO(file.stream.read().decode('utf-8'))
            reader = csv.DictReader(stream)
            count = 0
            
            for row in reader:
                mentee_email = row.get('mentee_email', '').strip()
                if not mentee_email:
                    continue
                
                mentee_user = MentorMenteeUser.query.filter_by(email=mentee_email).first()
                if mentee_user and mentee_user.role == 'mentee':
                    profile = MenteeProfile.query.filter_by(mentee_id=mentee_user.id).first()
                    if profile:
                        profile.assigned_mentor_id = mentor_id
                        count += 1
            
            db.session.commit()
            flash(f'Assigned {count} mentees!', 'success')
            return redirect(url_for('mentor_mentee.mentor_dashboard'))
        
        except Exception as e:
            current_app.logger.error(f"Error uploading mentees: {str(e)}")
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('mentor_mentee.mentor_upload_mentees'))
    
    return render_template('mentor_mentee/mentor_upload_mentees.html')

@mm_bp.route('/mentor/dashboard')
def mentor_dashboard():
    """Mentor sees their assigned mentees"""
    if session.get('user_role') != 'mentor':
        flash('Mentor access only', 'error')
        return redirect(url_for('mentor_mentee.login'))
    
    mentor_id = session.get('user_id')
    my_mentees = MenteeProfile.query.filter_by(assigned_mentor_id=mentor_id).all()
    
    return render_template('mentor_mentee/mentor_dashboard.html', mentees=my_mentees)

@mm_bp.route('/mentor/review-monthly/<int:form_id>', methods=['GET', 'POST'])
def mentor_review_monthly(form_id):
    """Mentor reviews mentee's monthly form"""
    if session.get('user_role') != 'mentor':
        flash('Mentor access only', 'error')
        return redirect(url_for('mentor_mentee.login'))
    
    form = MenteeMonthlyForm.query.get(form_id)
    if not form:
        flash('Form not found', 'error')
        return redirect(url_for('mentor_mentee.mentor_dashboard'))
    
    if request.method == 'POST':
        form.mentor_feedback = request.form.get('feedback')
        form.mentor_rating = int(request.form.get('rating', 0))
        form.status = 'reviewed'
        form.reviewed_date = db.func.now()
        db.session.commit()
        flash('Review submitted!', 'success')
        return redirect(url_for('mentor_mentee.mentor_dashboard'))
    
    return render_template('mentor_mentee/mentor_review_monthly.html', form=form)

@mm_bp.route('/mentor/review-yearly/<int:form_id>', methods=['GET', 'POST'])
def mentor_review_yearly(form_id):
    """Mentor reviews mentee's yearly form"""
    if session.get('user_role') != 'mentor':
        flash('Mentor access only', 'error')
        return redirect(url_for('mentor_mentee.login'))
    
    form = MenteeYearlyForm.query.get(form_id)
    if not form:
        flash('Form not found', 'error')
        return redirect(url_for('mentor_mentee.mentor_dashboard'))
    
    if request.method == 'POST':
        form.mentor_feedback = request.form.get('feedback')
        form.mentor_rating = int(request.form.get('rating', 0))
        form.status = 'reviewed'
        form.reviewed_date = db.func.now()
        db.session.commit()
        flash('Review submitted!', 'success')
        return redirect(url_for('mentor_mentee.mentor_dashboard'))
    
    return render_template('mentor_mentee/mentor_review_yearly.html', form=form)

# ==================== MENTEE ROUTES ====================

@mm_bp.route('/mentee/dashboard')
def mentee_dashboard():
    """Mentee sees their profile, mentor, and forms"""
    if session.get('user_role') != 'mentee':
        flash('Mentee access only', 'error')
        return redirect(url_for('mentor_mentee.login'))
    
    user_id = session.get('user_id')
    user = MentorMenteeUser.query.get(user_id)
    profile = MenteeProfile.query.filter_by(mentee_id=user_id).first()
    
    mentor = None
    mentor_profile = None
    if profile and profile.assigned_mentor_id:
        mentor = MentorMenteeUser.query.get(profile.assigned_mentor_id)
        mentor_profile = MentorProfile.query.filter_by(mentor_id=profile.assigned_mentor_id).first()
    
    monthly_forms = MenteeMonthlyForm.query.filter_by(mentee_id=user_id).all()
    yearly_form = MenteeYearlyForm.query.filter_by(mentee_id=user_id).first()
    
    return render_template('mentor_mentee/mentee_dashboard.html',
                          user=user,
                          profile=profile,
                          mentor=mentor,
                          mentor_profile=mentor_profile,
                          monthly_forms=monthly_forms,
                          yearly_form=yearly_form)

@mm_bp.route('/mentee/submit-monthly', methods=['GET', 'POST'])
def mentee_submit_monthly():
    """Mentee submits monthly form"""
    if session.get('user_role') != 'mentee':
        flash('Mentee access only', 'error')
        return redirect(url_for('mentor_mentee.login'))
    
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        form = MenteeMonthlyForm(
            mentee_id=user_id,
            month_year=request.form.get('month_year'),
            learning_progress=request.form.get('learning_progress'),
            challenges=request.form.get('challenges'),
            goals_this_month=request.form.get('goals_this_month'),
            status='submitted'
        )
        db.session.add(form)
        db.session.commit()
        flash('Monthly form submitted!', 'success')
        return redirect(url_for('mentor_mentee.mentee_dashboard'))
    
    return render_template('mentor_mentee/mentee_submit_monthly.html')

@mm_bp.route('/mentee/submit-yearly', methods=['GET', 'POST'])
def mentee_submit_yearly():
    """Mentee submits yearly form"""
    if session.get('user_role') != 'mentee':
        flash('Mentee access only', 'error')
        return redirect(url_for('mentor_mentee.login'))
    
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        form = MenteeYearlyForm(
            mentee_id=user_id,
            year=int(request.form.get('year')),
            summary_of_progress=request.form.get('summary_of_progress'),
            achievements=request.form.get('achievements'),
            challenges_over_year=request.form.get('challenges_over_year'),
            status='submitted'
        )
        db.session.add(form)
        db.session.commit()
        flash('Yearly form submitted!', 'success')
        return redirect(url_for('mentor_mentee.mentee_dashboard'))
    
    return render_template('mentor_mentee/mentee_submit_yearly.html')

# ==================== AUTH ROUTES ====================

@mm_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login for mentor/mentee/admin"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = MentorMenteeUser.query.filter_by(email=email).first()
        
        if not user:
            flash('Email not found. Contact admin.', 'error')
            return redirect(url_for('mentor_mentee.login'))
        
        if not user.check_password(password):
            flash('Wrong password', 'error')
            return redirect(url_for('mentor_mentee.login'))
        
        session['user_id'] = user.id
        session['user_role'] = user.role
        session['user_email'] = user.email
        session['user_name'] = user.name
        
        flash(f'Welcome, {user.name}!', 'success')
        
        if user.role == 'admin':
            return redirect(url_for('mentor_mentee.admin_dashboard'))
        elif user.role == 'mentor':
            return redirect(url_for('mentor_mentee.mentor_dashboard'))
        else:
            return redirect(url_for('mentor_mentee.mentee_dashboard'))
    
    return render_template('mentor_mentee/login.html')

@mm_bp.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('Logged out', 'success')
    return redirect(url_for('mentor_mentee.login'))

@mm_bp.route('/')
def index():
    """Landing page"""
    return render_template('mentor_mentee/index.html')
