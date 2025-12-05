from app import app, db, Tutor

def update_tutor():
    with app.app_context():
        tutor = Tutor.query.filter_by(email='tutor@school.edu').first()
        if tutor:
            print(f"Found tutor: {tutor.full_name}")
            tutor.email = 'drjenkins.greenwood@gmail.com'
            tutor.full_name = 'Dr. Sarah Jenkins'  # Updating name to match 'dr' in email
            db.session.commit()
            print("✅ Updated tutor email to drjenkins.greenwood@gmail.com and name to Dr. Sarah Jenkins")
        else:
            print("❌ Tutor with email tutor@school.edu not found.")
            
            # Check if already updated
            tutor_new = Tutor.query.filter_by(email='drjenkins.greenwood@gmail.com').first()
            if tutor_new:
                print("Tutor already exists with new email.")

if __name__ == "__main__":
    update_tutor()
