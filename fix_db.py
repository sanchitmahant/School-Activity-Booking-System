from app import app, db
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as conn:
        columns_to_add = [
            ("linkedin_url", "VARCHAR(200)"),
            ("years_experience", "INTEGER"),
            ("education", "TEXT"),
            ("certifications", "TEXT"),
            ("teaching_philosophy", "TEXT")
        ]

        for col_name, col_type in columns_to_add:
            try:
                print(f"Adding column {col_name}...")
                conn.execute(text(f"ALTER TABLE tutor ADD COLUMN {col_name} {col_type}"))
                print(f"Added {col_name}")
            except Exception as e:
                # SQLite throws OperationalError if column exists
                if "duplicate column name" in str(e):
                    print(f"Column {col_name} already exists.")
                else:
                    print(f"Error adding {col_name}: {e}")
        
        conn.commit()
        print("Database schema update complete.")
