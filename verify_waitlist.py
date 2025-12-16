import sys
import os
from app import app, db, Parent, Child, Activity, Booking, Waitlist, Tutor
from datetime import datetime, timedelta
from sqlalchemy import text

def verify_waitlist():
    print(f"DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Instance Path: {app.instance_path}")
    print("Setting up test data...")
    with app.app_context():
        print(f"Engine URL: {db.engine.url}")
        result = db.session.execute(text("PRAGMA table_info(booking)"))
        print("Booking Table Schema seen by script:")
        for row in result:
            print(row)
        # Create test tutor
        tutor = Tutor.query.filter_by(email="waitlist_tutor@test.com").first()
        if not tutor:
            tutor = Tutor(full_name="Waitlist Tutor", email="waitlist_tutor@test.com", password="pass", specialization="Test")
            db.session.add(tutor)
            db.session.commit()

        # Create test activity with capacity 1
        activity = Activity(
            name="Exclusive Class",
            description="Only 1 spot",
            price=10.0,
            day_of_week="Monday",
            start_time="10:00",
            end_time="11:00",
            max_capacity=1,
            tutor_id=tutor.id
        )
        db.session.add(activity)
        db.session.commit()
        print(f"Created Activity: {activity.name} (ID: {activity.id})")

        # Create 2 test children
        parent = Parent.query.filter_by(email="test@example.com").first()
        if not parent:
            print("Error: Test parent not found. Run init_db_script.py first.")
            return

        child1 = Child(name="Child A", age=10, grade="5", parent_id=parent.id)
        child2 = Child(name="Child B", age=10, grade="5", parent_id=parent.id)
        db.session.add_all([child1, child2])
        db.session.commit()
        print(f"Created Children: {child1.name} (ID: {child1.id}), {child2.name} (ID: {child2.id})")

        # Booking Date
        booking_date = datetime.now().date() + timedelta(days=7)

        # 1. Book with Child A
        print("\n1. Booking Child A...")
        booking1 = Booking(parent_id=parent.id, child_id=child1.id, activity_id=activity.id, booking_date=booking_date, status='confirmed', cost=activity.price)
        db.session.add(booking1)
        db.session.commit()
        print("Child A Booked.")

        # 2. Try to book Child B (Should be waitlisted)
        print("\n2. Adding Child B to Waitlist...")
        waitlist_entry = Waitlist(parent_id=parent.id, child_id=child2.id, activity_id=activity.id, request_date=booking_date)
        db.session.add(waitlist_entry)
        db.session.commit()
        print("Child B added to Waitlist.")

        # Verify Waitlist
        w_check = Waitlist.query.filter_by(activity_id=activity.id, child_id=child2.id).first()
        if w_check:
            print("VERIFIED: Child B is in Waitlist table.")
        else:
            print("FAILED: Child B not found in Waitlist.")

        # 3. Cancel Child A
        print("\n3. Cancelling Child A's booking (triggering promotion)...")
        # We need to call the actual logic. In app.py, this is done in the route. 
        # Here we verify the function `promote_waitlist_user` works.
        from app import promote_waitlist_user
        
        db.session.delete(booking1)
        db.session.commit()
        print("Child A booking deleted.")
        
        print("Calling promote_waitlist_user...")
        print("Calling promote_waitlist_user...")
        promoted = promote_waitlist_user(activity.id, booking_date)
        
        if promoted:
            # Verify the new booking
            new_booking = Booking.query.filter_by(activity_id=activity.id, booking_date=booking_date, status='confirmed').first()
            if new_booking and new_booking.child_id == child2.id:
                print(f"SUCCESS: Promoted user matches Child B ({child2.name})")
            else:
                print(f"FAILED: Expected Child B to be booked, but found {new_booking.child.name if new_booking else 'None'}")
        else:
            print("FAILED: Promotion function returned False")

        # 4. Verify Final State
        b_check = Booking.query.filter_by(child_id=child2.id, activity_id=activity.id).first()
        w_check_final = Waitlist.query.filter_by(child_id=child2.id, activity_id=activity.id).first()

        if b_check and b_check.status == 'confirmed':
            print("VERIFIED: Child B has a confirmed booking.")
        else:
            print("FAILED: Child B does not have a booking.")

        if w_check_final and w_check_final.status == 'promoted':
             print("VERIFIED: Child B waitlist status is 'promoted'.")
        elif not w_check_final:
             print("NOTE: Waitlist entry removed (acceptable implementation).")
        else:
             print(f"FAILED: Waitlist status is {w_check_final.status}")

        # Cleanup
        print("\nCleaning up...")
        if b_check: db.session.delete(b_check)
        if w_check_final: db.session.delete(w_check_final)
        db.session.delete(activity)
        db.session.delete(child1)
        db.session.delete(child2)
        db.session.delete(tutor)
        db.session.commit()
        print("Cleanup complete.")

if __name__ == "__main__":
    verify_waitlist()
