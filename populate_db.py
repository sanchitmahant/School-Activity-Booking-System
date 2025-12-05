"""
Database Population Script for Greenwood School Activity Booking System
Run this script to initialize the database with sample data
"""
from app import app, db, Admin, Parent, Tutor, Child, Activity
from werkzeug.security import generate_password_hash
from datetime import datetime

def populate_database():
    with app.app_context():
        # Drop all tables and recreate
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create Admin Users
        print("Creating admin users...")
        admin = Admin(
            email='greenwoodinternationaluk@gmail.com',
            password=generate_password_hash('admin123'),
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        
        # Create Test Parent
        print("Creating test parent...")
        parent = Parent(
            full_name='Test Parent',
            email='parent@test.com',
            password=generate_password_hash('parent123'),
            phone='1234567890',
            created_at=datetime.utcnow()
        )
        db.session.add(parent)
        db.session.flush() # Get parent ID
        
        # Create Test Children
        print("Creating test children...")
        child1 = Child(
            name='Emma Johnson',
            age=10,
            grade='Year 5',
            parent_id=parent.id
        )
        child2 = Child(
            name='Oliver Johnson',
            age=8,
            grade='Year 3',
            parent_id=parent.id
        )
        db.session.add_all([child1, child2])
        
        # Create Tutors
        print("Creating tutors...")
        tutors_data = [
            {
                'email': 'e.thompson@greenwood.edu',
                'password': 'tutor123',
                'full_name': 'Dr. Emily Thompson',
                'specialization': 'STEM & Robotics',
                'bio': 'PhD in Computer Science with 15 years of experience teaching robotics and programming to young minds.',
                'years_experience': 15,
                'education': 'PhD Computer Science, MIT',
                'certifications': 'STEM Education Specialist, Robotics Instructor Level 3',
                'teaching_philosophy': 'Learning through hands-on exploration and creative problem-solving'
            },
            {
                'email': 'j.martinez@greenwood.edu',
                'password': 'tutor123',
                'full_name': 'Professor James Martinez',
                'specialization': 'Music & Orchestra',
                'bio': 'Conductor with 20 years of experience, former member of London Symphony Orchestra.',
                'years_experience': 20,
                'education': 'MMus Performance, Royal Academy of Music',
                'certifications': 'Advanced Conducting Diploma, Music Theory Grade 8',
                'teaching_philosophy': 'Fostering musicality and ensemble skills through collaborative performance'
            },
            {
                'email': 's.williams@greenwood.edu',
                'password': 'tutor123',
                'full_name': 'Ms. Sarah Williams',
                'specialization': 'Fine Arts',
                'bio': 'Award-winning artist specializing in contemporary techniques and creative expression.',
                'years_experience': 12,
                'education': 'BFA Fine Arts, Central Saint Martins',
                'certifications': 'Art Therapy Practitioner, Portfolio Development Specialist',
                'teaching_philosophy': 'Encouraging individual artistic voice and experimental techniques'
            }
        ]
        
        for tutor_data in tutors_data:
            tutor = Tutor(
                email=tutor_data['email'],
                password=generate_password_hash(tutor_data['password']),
                full_name=tutor_data['full_name'],
                specialization=tutor_data['specialization'],
                bio=tutor_data['bio'],
                years_experience=tutor_data['years_experience'],
                education=tutor_data['education'],
                certifications=tutor_data['certifications'],
                teaching_philosophy=tutor_data['teaching_philosophy'],
                status='approved'
            )
            db.session.add(tutor)
        
        db.session.commit()
        
        # Get tutor IDs for activities
        robotics_tutor = Tutor.query.filter_by(specialization='STEM & Robotics').first()
        music_tutor = Tutor.query.filter_by(specialization='Music & Orchestra').first()
        art_tutor = Tutor.query.filter_by(specialization='Fine Arts').first()
        
        # Create Activities
        print("Creating activities...")
        activities_data = [
            {
                'name': 'Robotics Club',
                'description': 'Build and program robots using LEGO Mindstorms and Python',
                'day_of_week': 'Monday',
                'start_time': '15:00',
                'end_time': '17:00',
                'max_capacity': 12,
                'price': 35.00,
                'tutor_id': robotics_tutor.id if robotics_tutor else None
            },
            {
                'name': 'Chamber Orchestra',
                'description': 'Classical music ensemble for intermediate to advanced players',
                'day_of_week': 'Wednesday',
                'start_time': '16:00',
                'end_time': '18:00',
                'max_capacity': 20,
                'price': 45.00,
                'tutor_id': music_tutor.id if music_tutor else None
            },
            {
                'name': 'Fine Arts Studio',
                'description': 'Explore painting, sculpture, and mixed media techniques',
                'day_of_week': 'Friday',
                'start_time': '15:30',
                'end_time': '17:30',
                'max_capacity': 15,
                'price': 40.00,
                'tutor_id': art_tutor.id if art_tutor else None
            },
            {
                'name': 'Swimming',
                'description': 'Professional swimming lessons for all skill levels',
                'day_of_week': 'Tuesday',
                'start_time': '16:00',
                'end_time': '17:00',
                'max_capacity': 10,
                'price': 30.00,
                'tutor_id': None
            },
            {
                'name': 'Drama & Theatre',
                'description': 'Acting, improvisation, and stage performance skills',
                'day_of_week': 'Thursday',
                'start_time': '15:00',
                'end_time': '17:00',
                'max_capacity': 18,
                'price': 38.00,
                'tutor_id': None
            }
        ]
        
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.session.add(activity)
        
        db.session.commit()
        
        print("\n✅ Database populated successfully!")
        print(f"Created {Admin.query.count()} admins")
        print(f"Created {Parent.query.count()} parents")
        print(f"Created {Tutor.query.count()} tutors")
        print(f"Created {Activity.query.count()} activities")
        print(f"Created {Child.query.count()} children")
        print("\n📝 Test Credentials:")
        print("Admin: greenwoodinternationaluk@gmail.com / admin123")
        print("Parent: parent@test.com / parent123")
        print("Tutor: e.thompson@greenwood.edu / tutor123")

if __name__ == '__main__':
    populate_database()
