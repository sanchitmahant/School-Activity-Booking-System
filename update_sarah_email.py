"""
Quick script to update Dr. Sarah Jenkins' email in the existing database
"""
from app import app, db, Tutor

with app.app_context():
    # Find Dr. Sarah Jenkins
    sarah = Tutor.query.filter_by(full_name='Dr. Sarah Jenkins').first()
    
    if sarah:
        old_email = sarah.email
        sarah.email = 'drjenkins.greenwood@gmail.com'
        db.session.commit()
        print(f"✅ Updated Dr. Sarah Jenkins")
        print(f"   Old: {old_email}")
        print(f"   New: drjenkins.greenwood@gmail.com")
    else:
        print("❌ Dr. Sarah Jenkins not found in database")
        print("   You may need to run populate_db.py first")
