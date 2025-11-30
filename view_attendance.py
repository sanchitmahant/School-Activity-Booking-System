"""
Quick script to view attendance records in the database
"""
from app import app, db, Attendance, Child, Activity
from datetime import datetime

with app.app_context():
    print("📊 ATTENDANCE RECORDS\n" + "="*50 + "\n")
    
    records = Attendance.query.order_by(Attendance.date.desc()).all()
    
    if records:
        for record in records:
            child = Child.query.get(record.child_id)
            activity = Activity.query.get(record.activity_id)
            
            status_icon = {
                'present': '✅',
                'late': '⏰',
                'absent': '❌'
            }.get(record.status, '❓')
            
            print(f"{status_icon} {record.date} | {child.name} | {activity.name} | {record.status.upper()}")
    else:
        print("No attendance records found in database.")
        print("\nThis means:")
        print("1. Attendance was saved but the Attendance table doesn't exist")
        print("2. Or the route isn't actually saving to the database")
        print("\nLet me check if the table exists...")
        
        # Check if table exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'attendance' in tables:
            print("✅ Attendance table EXISTS")
            print("   The data should be there. Try marking attendance again.")
        else:
            print("❌ Attendance table DOES NOT EXIST!")
            print("   The table needs to be created first.")
