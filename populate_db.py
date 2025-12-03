"""
Database Population Script for Greenwood School Activity Booking System
Run this script to initialize the database with sample data
"""
from app import app, db, User, Child, Activity, Tutor
from werkzeug.security import generate_password_hash
from datetime import datetime, time

def populate_database():
    with app.app_context():
        # Drop all tables and recreate
        print("Creating database tables...")
        db.create_all()
        
        # Create Admin Users
        print("Creating admin users...")
        admin = User(
            username='admin',
            email='greenwoodinternationaluk@gmail.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        
        # Create Test Parent
        print("Creating test parent...")
        parent = User(
            username='parent1',
            email='parent@test.com',
            password_hash=generate_password_hash('parent123'),
            role='parent',
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(parent)
        
        # Create Test Children
        print("Creating test children...")
        child1 = Child(
            name='Emma Johnson',
            age=10,
            grade='Year 5',
            parent=parent
        )
        child2 = Child(
            name='Oliver Johnson',
            age=8,
            grade='Year 3',
            parent=parent
        )
        db.session.add_all([child1, child2])
        
        # Create Tutors
        print("Creating tutors...")
        tutors_data = [
            {
                'user': User(username='dr_thompson', email='e.thompson@greenwood.edu', 
                           password_hash=generate_password_hash('tutor123'), role='tutor', is_active=True),
                'name': 'Dr. Emily Thompson',
                'specialization': 'STEM & Robotics',
                'bio': 'PhD in Computer Science with 15 years of experience teaching robotics and programming to young minds.',
                'years_experience': 15,
                'education': 'PhD Computer Science, MIT',
                'certifications': 'STEM Education Specialist, Robotics Instructor Level 3',
                'teaching_philosophy': 'Learning through hands-on exploration and creative problem-solving'
            },
            {
                'user': User(username='prof_martinez', email='j.martinez@greenwood.edu', 
                           password_hash=generate_password_hash('tutor123'), role='tutor', is_active=True),
                'name': 'Professor James Martinez',
                'specialization': 'Music & Orchestra',
                'bio': 'Conductor with 20 years of experience, former member of London Symphony Orchestra.',
                'years_experience': 20,
                'education': 'MMus Performance, Royal Academy of Music',
                'certifications': 'Advanced Conducting Diploma, Music Theory Grade 8',
                'teaching_philosophy': 'Fostering musicality and ensemble skills through collaborative performance'
            },
            {
                'user': User(username='ms_williams', email='s.williams@greenwood.edu', 
                           password_hash=generate_password_hash('tutor123'), role='tutor', is_active=True),
                'name': 'Ms. Sarah Williams',
                'specialization': 'Fine Arts',
                'bio': 'Award-winning artist specializing in contemporary techniques and creative expression.',
                'years_experience': 12,
                'education': 'BFA Fine Arts, Central Saint Martins',
                'certifications': 'Art Therapy Practitioner, Portfolio Development Specialist',
                'teaching_philosophy': 'Encouraging individual artistic voice and experimental techniques'
            }
        ]
        
        for tutor_data in tutors_data:
            user = tutor_data['user']
            db.session.add(user)
            db.session.flush()  # Get the user ID
            
            tutor = Tutor(
                user_id=user.id,
                name=tutor_data['name'],
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
                'capacity': 12,
                'price': 35.00,
                'age_group': '8-14',
                'tutor_id': robotics_tutor.id if robotics_tutor else None
            },
            {
                'name': 'Chamber Orchestra',
                'description': 'Classical music ensemble for intermediate to advanced players',
                'day_of_week': 'Wednesday',
                'start_time': '16:00',
                'end_time': '18:00',
                'capacity': 20,
                'price': 45.00,
                'age_group': '10-16',
                'tutor_id': music_tutor.id if music_tutor else None
            },
            {
                'name': 'Fine Arts Studio',
                'description': 'Explore painting, sculpture, and mixed media techniques',
                'day_of_week': 'Friday',
                'start_time': '15:30',
                'end_time': '17:30',
                'capacity': 15,
                'price': 40.00,
                'age_group': '7-15',
                'tutor_id': art_tutor.id if art_tutor else None
            },
            {
                'name': 'Swimming',
                'description': 'Professional swimming lessons for all skill levels',
                'day_of_week': 'Tuesday',
                'start_time': '16:00',
                'end_time': '17:00',
                'capacity': 10,
                'price': 30.00,
                'age_group': '6-16',
                'tutor_id': None
            },
            {
                'name': 'Drama & Theatre',
                'description': 'Acting, improvisation, and stage performance skills',
                'day_of_week': 'Thursday',
                'start_time': '15:00',
                'end_time': '17:00',
                'capacity': 18,
                'price': 38.00,
                'age_group': '8-16',
                'tutor_id': None
            }
        ]
        
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.session.add(activity)
        
        db.session.commit()
        
        print("\n✅ Database populated successfully!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Tutor.query.count()} tutors")
        print(f"Created {Activity.query.count()} activities")
        print(f"Created {Child.query.count()} children")
        print("\n📝 Test Credentials:")
        print("Admin: admin / admin123")
        print("Parent: parent1 / parent123")
        print("Tutor: dr_thompson / tutor123")

if __name__ == '__main__':
    populate_database()
