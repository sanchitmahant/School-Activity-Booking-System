"""
Add LinkedIn and Professional Details to Tutor Schema
Systematic database update for professional tutor profiles
"""

import sqlite3

print("=" * 80)
print("ADDING PROFESSIONAL TUTOR DETAILS")
print("=" * 80)

conn = sqlite3.connect('booking_system_v2.db')
cursor = conn.cursor()

# Add new columns to Tutor table
new_columns = [
    ("linkedin_url", "TEXT"),
    ("years_experience", "INTEGER"),
    ("education", "TEXT"),
    ("certifications", "TEXT"),
    ("teaching_philosophy", "TEXT")
]

for column_name, column_type in new_columns:
    try:
        cursor.execute(f"ALTER TABLE Tutor ADD COLUMN {column_name} {column_type}")
        print(f"✅ Added column: {column_name}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"⚠️  Column {column_name} already exists")
        else:
            print(f"❌ Error adding {column_name}: {e}")

# Update existing tutors with professional LinkedIn profiles and details
professional_data = {
    "Dr. Sarah Jenkins": {
        "linkedin_url": "https://www.linkedin.com/in/sarah-jenkins-robotics-educator",
        "years_experience": 8,
        "education": "MEng Robotics, Imperial College London; PhD Mechanical Engineering, Cambridge",
        "certifications": "STEM Education Specialist, LEGO Education Certified Trainer",
        "teaching_philosophy": "I believe in hands-on, project-based learning where students learn by building and iterating. Every failure is a learning opportunity."
    },
    "James Rodriguez": {
        "linkedin_url": "https://www.linkedin.com/in/james-rodriguez-swim-coach",
        "years_experience": 15,
        "education": "BSc Sports Science, Loughborough University; ASA Level 2 Swimming Coach",
        "certifications": "ASA Level 2 Coach, Lifeguard Trainer, Sports Psychology Certificate",
        "teaching_philosophy": "Building water confidence and technical excellence through patience, encouragement, and structured progression."
    },
    "Emily Thompson": {
        "linkedin_url": "https://www.linkedin.com/in/emily-thompson-creative-writer",
        "years_experience": 12,
        "education": "MA Creative Writing, University of East Anglia; BA English Literature, Oxford",
        "certifications": "Published Author, Creative Writing Workshop Leader Certificate",
        "teaching_philosophy": "Every student has a unique voice. My role is to help them discover and refine it through exploration and constructive feedback."
    },
    "David Park": {
        "linkedin_url": "https://www.linkedin.com/in/david-park-software-engineer",
        "years_experience": 10,
        "education": "BSc Computer Science, University of Cambridge; MSc Artificial Intelligence, Imperial",
        "certifications": "Google Certified Educator, Python Institute Certified",
        "teaching_philosophy": "Coding is a creative endeavor. I teach problem-solving skills that transcend programming languages."
    }
}

for tutor_name, data in professional_data.items():
    try:
        cursor.execute("""
            UPDATE Tutor 
            SET linkedin_url = ?,
                years_experience = ?,
                education = ?,
                certifications = ?,
                teaching_philosophy = ?
            WHERE full_name = ?
        """, (
            data['linkedin_url'],
            data['years_experience'],
            data['education'],
            data['certifications'],
            data['teaching_philosophy'],
            tutor_name
        ))
        if cursor.rowcount > 0:
            print(f"✅ Updated professional details for: {tutor_name}")
    except Exception as e:
        print(f"❌ Error updating {tutor_name}: {e}")

conn.commit()
conn.close()

print("\n✅ Professional tutor details added successfully!")
print("=" * 80)
