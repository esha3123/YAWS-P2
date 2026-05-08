#!/usr/bin/env python
"""
Flask CLI commands for Mentor-Mentee system
Run: flask init-mm
"""

from flask import current_app
from flask.cli import with_appcontext
import click
from app.mentor_mentee.models import MentorMenteeUser, MentorProfile, MenteeProfile

def register_cli_commands(app):
    """Register CLI commands with Flask app"""
    
    @app.cli.command()
    @with_appcontext
    def init_mm():
        """Initialize Mentor-Mentee system with default admin"""
        from app.models.models import db
        
        # Create tables
        db.create_all()
        
        # Check if admin exists
        admin = MentorMenteeUser.query.filter_by(email='admin@college.edu').first()
        
        if admin:
            click.echo("⚠️  Admin already exists!")
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
        
        click.echo("\n" + "="*50)
        click.echo("✅ MENTOR-MENTEE SYSTEM INITIALIZED")
        click.echo("="*50)
        click.echo("\n📧 DEFAULT ADMIN CREATED:")
        click.echo("   Email:    admin@college.edu")
        click.echo("   Password: admin123")
        click.echo("\n🔗 Start app: python run.py")
        click.echo("   Then login: http://127.0.0.1:5000/mentor-mentee/login")
        click.echo("="*50 + "\n")
    
    @app.cli.command()
    @with_appcontext
    def reset_mm():
        """⚠️ DANGEROUS: Reset mentor-mentee system (delete all data)"""
        from app.models.models import db
        
        if click.confirm('⚠️  This will DELETE all mentor-mentee data. Continue?'):
            MenteeProfile.query.delete()
            MentorProfile.query.delete()
            MenteeMonthlyForm.query.delete()
            MenteeYearlyForm.query.delete()
            MentorMenteeUser.query.delete()
            db.session.commit()
            
            click.echo("✅ All mentor-mentee data deleted!")
            
            # Recreate admin
            new_admin = MentorMenteeUser(
                email='admin@college.edu',
                name='System Administrator',
                role='admin',
                verified=True
            )
            new_admin.set_password('admin123')
            db.session.add(new_admin)
            db.session.commit()
            
            click.echo("✅ Default admin recreated")
        else:
            click.echo("❌ Cancelled")
