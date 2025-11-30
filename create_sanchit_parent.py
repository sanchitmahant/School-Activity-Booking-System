"""
Create parent profile for Sanchit Kaushal
"""
from app import app, db, Parent, Child

with app.app_context():
    # Check if parent already exists
    existing = Parent.query.filter_by(email='sanchitmahant@gmail.com').first()
    if existing:
        print("❌ Parent already exists!")
        print(f"   Email: {existing.email}")
        print(f"   Name: {existing.full_name}")
    else:
        # Create parent
        parent = Parent(
            email='sanchitmahant@gmail.com',
            full_name='Sanchit Kaushal',
            phone='07700900000'
        )
        parent.set_password('sanchitkaushal123')
        db.session.add(parent)
        db.session.commit()
        
        # Create child
        child = Child(
            parent_id=parent.id,
            name='Aryan Kaushal',
            age=8,
            grade='3'
        )
        db.session.add(child)
        db.session.commit()
        
        print("✅ Parent profile created!")
        print(f"\n📧 Login Details:")
        print(f"   Email: sanchitmahant@gmail.com")
        print(f"   Password: sanchitkaushal123")
        print(f"   URL: http://127.0.0.1:5000/login")
        print(f"\n👶 Child Created:")
        print(f"   Name: Aryan Kaushal")
        print(f"   Age: 8")
        print(f"   Grade: 3")
