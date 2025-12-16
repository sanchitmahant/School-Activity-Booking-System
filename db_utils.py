"""
Database utilities and initialization helpers
"""
from app import app, db, Parent, Child, Activity, Booking, Admin, Tutor, Waitlist, Attendance
from datetime import datetime, date, timedelta

def init_database():
    """Initialize database with all tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

def seed_demo_data():
    """Seed database with demo data for testing"""
    with app.app_context():
        # Check if demo data already exists
        if Parent.query.filter_by(email='demo@example.com').first():
            print("⚠️  Demo data already exists. Skipping seeding.")
            return
        
        # Create demo parent
        demo_parent = Parent(
            email='demo@example.com',
            full_name='Demo Parent',
            phone='(555) 123-4567'
        )
        demo_parent.set_password('demo123')
        db.session.add(demo_parent)
        db.session.commit()
        print("✅ Demo parent created (demo@example.com / demo123)")
        
        # Create demo children
        children_data = [
            {'name': 'Emma Johnson', 'age': 10, 'grade': '5th'},
            {'name': 'Liam Johnson', 'age': 8, 'grade': '3rd'},
            {'name': 'Sophia Johnson', 'age': 12, 'grade': '7th'},
        ]
        
        for child_data in children_data:
            child = Child(
                parent_id=demo_parent.id,
                name=child_data['name'],
                age=child_data['age'],
                grade=child_data['grade']
            )
            db.session.add(child)
        db.session.commit()
        print("✅ Demo children created (3 children)")
        
        # Create activities if they don't exist
        if Activity.query.count() == 0:
            activities_data = [
                {
                    'name': 'Soccer',
                    'description': 'Fun soccer training session for kids. Learn basic skills and teamwork.',
                    'price': 20.0,
                    'max_capacity': 15,
                    'day_of_week': 'Monday',
                    'start_time': '15:00',
                    'end_time': '16:30'
                },
                {
                    'name': 'Basketball',
                    'description': 'Basketball skills development for all levels.',
                    'price': 20.0,
                    'max_capacity': 12,
                    'day_of_week': 'Tuesday',
                    'start_time': '15:00',
                    'end_time': '16:30'
                },
                {
                    'name': 'Art Class',
                    'description': 'Creative art and painting class. Express your creativity!',
                    'price': 15.0,
                    'max_capacity': 20,
                    'day_of_week': 'Wednesday',
                    'start_time': '15:00',
                    'end_time': '16:30'
                },
                {
                    'name': 'Chess Club',
                    'description': 'Learn and play chess. Improve strategic thinking.',
                    'price': 10.0,
                    'max_capacity': 25,
                    'day_of_week': 'Thursday',
                    'start_time': '15:00',
                    'end_time': '16:30'
                },
                {
                    'name': 'Music Lessons',
                    'description': 'Piano and guitar lessons for beginners and intermediate players.',
                    'price': 30.0,
                    'max_capacity': 10,
                    'day_of_week': 'Friday',
                    'start_time': '15:00',
                    'end_time': '16:30'
                },
                {
                    'name': 'Swimming',
                    'description': 'Swimming lessons and water safety training.',
                    'price': 25.0,
                    'max_capacity': 8,
                    'day_of_week': 'Monday',
                    'start_time': '16:45',
                    'end_time': '17:45'
                },
                {
                    'name': 'Coding Club',
                    'description': 'Introduction to coding and computer science.',
                    'price': 25.0,
                    'max_capacity': 15,
                    'day_of_week': 'Wednesday',
                    'start_time': '16:45',
                    'end_time': '17:45'
                },
                {
                    'name': 'Robotics',
                    'description': 'Build and program robots. Hands-on STEM learning.',
                    'price': 35.0,
                    'max_capacity': 10,
                    'day_of_week': 'Friday',
                    'start_time': '16:45',
                    'end_time': '17:45'
                },
            ]
            
            for activity_data in activities_data:
                activity = Activity(**activity_data)
                db.session.add(activity)
            db.session.commit()
            print(f"✅ {len(activities_data)} activities created")
        
        # Create demo bookings for the next 30 days
        try:
            demo_child = demo_parent.children[0]
            demo_activity = Activity.query.first()
            
            # Book for next Monday
            next_monday = datetime.now().date()
            while next_monday.weekday() != 0:  # 0 = Monday
                next_monday += timedelta(days=1)
            
            demo_booking = Booking(
                parent_id=demo_parent.id,
                child_id=demo_child.id,
                activity_id=demo_activity.id,
                booking_date=next_monday,
                cost=demo_activity.price,
                status='confirmed'
            )
            db.session.add(demo_booking)
            db.session.commit()
            print(f"✅ Demo booking created for {demo_child.name}")
        except Exception as e:
            print(f"⚠️  Could not create demo booking: {e}")
        
        print("\n🎉 Database seeding completed successfully!")

def reset_database():
    """Delete all tables and recreate them (WARNING: Destructive)"""
    with app.app_context():
        confirm = input("⚠️  This will delete all data. Are you sure? (yes/no): ")
        if confirm.lower() == 'yes':
            db.drop_all()
            print("❌ All tables dropped")
            db.create_all()
            print("✅ New tables created")
        else:
            print("❌ Operation cancelled")

def get_database_stats():
    """Print database statistics"""
    with app.app_context():
        print("\n📊 Database Statistics")
        print("-" * 40)
        print(f"Parents: {Parent.query.count()}")
        print(f"Children: {Child.query.count()}")
        print(f"Activities: {Activity.query.count()}")
        print(f"Bookings: {Booking.query.count()}")
        
        # Calculate total revenue
        total_revenue = db.session.query(db.func.sum(Booking.cost)).filter(
            Booking.status == 'confirmed'
        ).scalar() or 0
        print(f"Total Revenue (Confirmed): ${total_revenue:.2f}")
        print("-" * 40 + "\n")

if __name__ == '__main__':
    import sys
    
    print("🎯 School Activity Booking System - Database Utilities\n")
    
    if len(sys.argv) < 2:
        print("Usage: python db_utils.py [command]")
        print("\nAvailable commands:")
        print("  init    - Initialize database")
        print("  seed    - Seed database with demo data")
        print("  reset   - Reset database (WARNING: Destructive)")
        print("  stats   - Show database statistics")
    else:
        command = sys.argv[1].lower()
        
        if command == 'init':
            init_database()
        elif command == 'seed':
            init_database()
            seed_demo_data()
        elif command == 'reset':
            reset_database()
        elif command == 'stats':
            get_database_stats()
        else:
            print(f"❌ Unknown command: {command}")
