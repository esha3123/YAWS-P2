#!/usr/bin/env python
"""Setup script - Run once to initialize the system"""

from app import create_app, db
from app.mentor_mentee.models import MentorMenteeUser, MenteeProfile, MentorProfile

def init_system():
    """Initialize system with default admin if not exists"""
    app = create_app()
    
    with app.app_context():
        # Check if admin exists
        admin = MentorMenteeUser.query.filter_by(email='admin@college.edu').first()
        
        if admin:
            print("✅ Admin already exists")
            return
        
        # Create default admin
        new_admin = MentorMenteeUser(
            email='admin@college.edu',
            name='System Administrator',
            role='admin',
            verified=True
        )
        new_admin.set_password('admin123')
        db.session.add(new_admin)
        db.session.commit()
        
        print("\n" + "="*50)
        print("✅ SYSTEM INITIALIZED")
        print("="*50)
        print("\n📧 DEFAULT ADMIN CREATED:")
        print("   Email:    admin@college.edu")
        print("   Password: admin123")
        print("\n🔗 Login at: http://127.0.0.1:5000/mentor-mentee/login")
        print("="*50 + "\n")

if __name__ == '__main__':
    init_system()
