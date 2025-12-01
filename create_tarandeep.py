"""
Create Tarandeep Singh parent account with child Jangbaaz Singh
"""
from app import app, db, Parent, Child
from werkzeug.security import generate_password_hash

def create_tarandeep():
    with app.app_context():
        # Check if parent already exists
        existing = Parent.query.filter_by(email='taranjob321@gmail.com').first()
        if existing:
            print("⚠️  Parent already exists!")
            print(f"   Email: {existing.email}")
            print(f"   Name: {existing.full_name}")
            return
        
        # Create parent
        parent = Parent(
            email='taranjob321@gmail.com',
            full_name='Tarandeep Singh',
            phone='07987654321',
            password_hash=generate_password_hash('123tarandeep')
        )
        db.session.add(parent)
        db.session.commit()
        
        print("✅ Created parent account:")
        print(f"   Name: Tarandeep Singh")
        print(f"   Email: taranjob321@gmail.com")
        print(f"   Password: 123tarandeep")
        print(f"   ID: {parent.id}")
        
        # Create child
        child = Child(
            name='Jangbaaz Singh',
            age=10,
            grade=5,
            parent_id=parent.id
        )
        db.session.add(child)
        db.session.commit()
        
        print("\n✅ Created child:")
        print(f"   Name: Jangbaaz Singh")
        print(f"   Age: 10")
        print(f"   Grade: 5")
        print(f"   ID: {child.id}")
        
        print("\n🎉 All done! You can now login at http://localhost:5000/login")

if __name__ == '__main__':
    create_tarandeep()
