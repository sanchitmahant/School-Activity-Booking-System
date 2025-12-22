"""
Database Initialization Script
Safely creates database and tables with sample data
"""
from app import app, db
from app import Admin, Parent, Child, Activity, Tutor, Booking
from datetime import datetime, timedelta
import os

def init_database():
    """Initialize database with tables and sample data"""
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully")
        
        # Check if admin already exists
        if not Admin.query.first():
            print("\nCreating default admin account...")
            admin = Admin(email='admin@greenwood.edu')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin account created")
            print("  Email: admin@greenwood.edu")
            print("  Password: admin123")
        else:
            print("✓ Admin account already exists")
        
        # Check if sample activities exist
        if Activity.query.count() == 0:
            print("\nCreating sample activities...")
            
            # Create sample tutor first
            if not Tutor.query.first():
                tutor = Tutor(
                    email='tutor@greenwood.edu',
                    full_name='John Smith',
                    specialization='Mathematics',
                    qualification='MSc Mathematics',
                    experience_years=5,
                    certifications='Certified Teacher',
                    teaching_philosophy='Student-centered learning',
                    bio='Experienced educator passionate about making math fun',
                    status='approved'
                )
                tutor.set_password('tutor123')
                db.session.add(tutor)
                db.session.commit()
                print("✓ Sample tutor created")
            
            tutor = Tutor.query.first()
            
            activities = [
                Activity(
                    name='Soccer Training',
                    description='Build skills and teamwork on the field',
                    day_of_week='Monday',
                    start_time='15:00',
                    end_time='16:30',
                    price=25.00,
                    max_capacity=15,
                    current_bookings=0,
                    tutor_id=tutor.id
                ),
                Activity(
                    name='Music Lessons',
                    description='Piano and guitar lessons for beginners',
                    day_of_week='Tuesday',
                    start_time='16:00',
                    end_time='17:00',
                    price=30.00,
                    max_capacity=8,
                    current_bookings=0,
                    tutor_id=tutor.id
                ),
                Activity(
                    name='Art Workshop',
                    description='Creative painting and drawing',
                    day_of_week='Wednesday',
                    start_time='15:30',
                    end_time='17:00',
                    price=20.00,
                    max_capacity=12,
                    current_bookings=0,
                    tutor_id=tutor.id
                ),
                Activity(
                    name='Coding Club',
                    description='Learn Python programming basics',
                    day_of_week='Thursday',
                    start_time='15:00',
                    end_time='16:30',
                    price=35.00,
                    max_capacity=10,
                    current_bookings=0,
                    tutor_id=tutor.id
                ),
                Activity(
                    name='Drama & Theatre',
                    description='Build confidence through performing arts',
                    day_of_week='Friday',
                    start_time='16:00',
                    end_time='17:30',
                    price=25.00,
                    max_capacity=15,
                    current_bookings=0,
                    tutor_id=tutor.id
                )
            ]
            
            for activity in activities:
                db.session.add(activity)
            
            db.session.commit()
            print(f"✓ Created {len(activities)} sample activities")
        else:
            print("✓ Sample activities already exist")
        
        print("\n" + "="*50)
        print("DATABASE INITIALIZATION COMPLETE!")
        print("="*50)
        print("\nDefault Accounts:")
        print("  Admin: admin@greenwood.edu / admin123")
        print("  Tutor: tutor@greenwood.edu / tutor123")
        print("\nYou can now run the application with: run.bat")
        print("="*50)

if __name__ == '__main__':
    init_database()

# Database Schema Checked

