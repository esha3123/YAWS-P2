#!/usr/bin/env python
"""Script to create test users (mentee, mentor)"""

from app import create_app, db
from app.mentor_mentee.models import MentorMenteeUser, MenteeProfile, MentorProfile

app = create_app()

with app.app_context():
    # Create test mentor
    mentor = MentorMenteeUser.query.filter_by(email='mentor@college.edu').first()
    if not mentor:
        mentor = MentorMenteeUser(
            email='mentor@college.edu',
            name='Dr. Rajesh Kumar',
            role='mentor',
            verified=True
        )
        mentor.set_password('mentor123')
        db.session.add(mentor)
        db.session.flush()
        
        mentor_profile = MentorProfile(
            mentor_id=mentor.id,
            department='Computer Science',
            subject='Python Programming',
            bio='Experienced mentor with 10 years of teaching',
            experience_years=10
        )
        db.session.add(mentor_profile)
        print("✅ Mentor created: mentor@college.edu / mentor123")
    else:
        print("⚠️  Mentor already exists")
    
    # Create test mentee
    mentee = MentorMenteeUser.query.filter_by(email='student@college.edu').first()
    if not mentee:
        mentee = MentorMenteeUser(
            email='student@college.edu',
            name='John Doe',
            role='mentee',
            verified=True
        )
        mentee.set_password('student123')
        db.session.add(mentee)
        db.session.flush()
        
        # Get mentor ID if exists
        mentor_obj = MentorMenteeUser.query.filter_by(email='mentor@college.edu').first()
        
        mentee_profile = MenteeProfile(
            mentee_id=mentee.id,
            department='Computer Science',
            year=2,
            roll_no='23001',
            assigned_mentor_id=mentor_obj.id if mentor_obj else None
        )
        db.session.add(mentee_profile)
        print("✅ Mentee created: student@college.edu / student123")
    else:
        print("⚠️  Mentee already exists")
    
    db.session.commit()
    
    print("\n" + "="*50)
    print("TEST USERS CREATED")
    print("="*50)
    print("\n📌 MENTOR:")
    print("   Email: mentor@college.edu")
    print("   Pass:  mentor123")
    print("\n📌 MENTEE:")
    print("   Email: student@college.edu")
    print("   Pass:  student123")
    print("\n🔗 Login: http://127.0.0.1:5000/mentor-mentee/login")
    print("="*50)
