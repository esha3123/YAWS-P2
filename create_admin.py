#!/usr/bin/env python
"""Script to create admin user manually"""

from app import create_app, db
from app.mentor_mentee.models import MentorMenteeUser, MentorProfile

app = create_app()

with app.app_context():
    # Check if admin already exists
    admin = MentorMenteeUser.query.filter_by(email='admin@college.edu').first()
    
    if admin:
        print("❌ Admin already exists!")
        print(f"Email: {admin.email}")
        print(f"Role: {admin.role}")
    else:
        # Create new admin
        new_admin = MentorMenteeUser(
            email='admin@college.edu',
            name='System Administrator',
            role='admin',
            verified=True
        )
        new_admin.set_password('admin123')  # Set password
        
        db.session.add(new_admin)
        db.session.commit()
        
        print("✅ Admin created successfully!")
        print("\n📧 Login Credentials:")
        print("=" * 40)
        print(f"Email:    admin@college.edu")
        print(f"Password: admin123")
        print("=" * 40)
        print("\n🔗 Go to: http://127.0.0.1:5000/mentor-mentee/login")
