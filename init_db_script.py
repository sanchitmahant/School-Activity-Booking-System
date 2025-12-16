from app import app, db, Admin, Tutor, Parent, Activity
import os

# Use drop_all for clean reset
with app.app_context():
    print(f"DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    db.drop_all()
    print("Dropped old tables.")
    db.create_all()
    print("Created tables.")

    # Admin
    admin = Admin(email='admin@school.edu')
    admin.set_password('admin123')
    db.session.add(admin)

    # Tutor
    tutor = Tutor(email='tutor@school.edu', full_name='Sarah Jenkins', specialization='Science & Robotics')
    tutor.set_password('tutor123')
    db.session.add(tutor)

    # Parent
    parent = Parent(email='test@example.com', full_name='Test User', phone='1234567890')
    parent.set_password('password123')
    db.session.add(parent)
    
    db.session.commit()
    print("Created Users: Admin, Tutor, Parent.")

    # Activities
    tutor = Tutor.query.filter_by(email='tutor@school.edu').first()
    activities = [
        Activity(name='Robotics Club', description='Build robots', price=50.0, day_of_week='Monday', start_time='15:00', end_time='16:30', tutor_id=tutor.id),
        Activity(name='Swimming', description='Pool time', price=30.0, day_of_week='Tuesday', start_time='15:00', end_time='16:30', tutor_id=tutor.id),
    ]
    db.session.add_all(activities)
    db.session.commit()
    print("Created Activities.")
