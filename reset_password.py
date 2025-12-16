from app import app, db, Parent

def reset_password(email, new_password):
    with app.app_context():
        user = Parent.query.filter_by(email=email).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
            print(f"Password for {email} has been reset to: {new_password}")
        else:
            print(f"User with email {email} not found.")

if __name__ == "__main__":
    reset_password("sanchitmahant@gmail.com", "password123")
