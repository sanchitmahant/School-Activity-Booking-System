"""
Update database schema to add tutor approval fields
RUN THIS ONCE to update existing database
"""
from app import app, db, Tutor
from sqlalchemy import text

with app.app_context():
    print("🔄 Updating database schema...")
    
    # Add new columns to tutor table
    try:
        with db.engine.connect() as conn:
            # Check if columns exist first
            result = conn.execute(text("PRAGMA table_info(tutor)"))
            columns = [row[1] for row in result]
            
            if 'status' not in columns:
                conn.execute(text("ALTER TABLE tutor ADD COLUMN status VARCHAR(20) DEFAULT 'pending'"))
                print("✅ Added 'status' column")
            
            if 'application_date' not in columns:
                conn.execute(text("ALTER TABLE tutor ADD COLUMN application_date DATETIME"))
                print("✅ Added 'application_date' column")
            
            if 'approved_by' not in columns:
                conn.execute(text("ALTER TABLE tutor ADD COLUMN approved_by INTEGER"))
                print("✅ Added 'approved_by' column")
            
            if 'approval_date' not in columns:
                conn.execute(text("ALTER TABLE tutor ADD COLUMN approval_date DATETIME"))
                print("✅ Added 'approval_date' column")
            
            if 'email_verified' not in columns:
                conn.execute(text("ALTER TABLE tutor ADD COLUMN email_verified BOOLEAN DEFAULT 0"))
                print("✅ Added 'email_verified' column")
            
            conn.commit()
        
        # Update existing tutors to 'approved' status
        existing_tutors = Tutor.query.all()
        for tutor in existing_tutors:
            if not hasattr(tutor, 'status') or tutor.status is None:
                tutor.status = 'approved'  # Existing tutors are auto-approved
                tutor.email_verified = True
        db.session.commit()
        print(f"✅ Updated {len(existing_tutors)} existing tutors to 'approved' status")
        
        print("\n🎉 Database schema updated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Note: If columns already exist, this error can be ignored.")
