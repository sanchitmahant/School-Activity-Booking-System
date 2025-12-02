"""
Update existing tutor profiles with complete professional data
"""
from app import app, db, Tutor

# Professional data for each tutor
tutor_data = {
    "Dr. Sarah Jenkins": {
        "linkedin_url": "https://linkedin.com/in/sarah-jenkins-robotics-educator",
        "years_experience": 8,
        "education": "MEng Robotics (Imperial College London), PhD Mechanical Engineering (University of Cambridge)",
        "certifications": "STEM Education Specialist, LEGO Certified Trainer, First Robotics Competition Judge",
        "teaching_philosophy": "I believe in hands-on, project-based learning that empowers students to think creatively and solve real-world problems through engineering design.",
        "bio": "Dr. Jenkins spent 8 years as a robotics engineer at Dyson before transitioning to education. She leads students in national robotics competitions and has mentored teams to multiple championship titles."
    },
    "James Rodriguez": {
        "linkedin_url": "https://linkedin.com/in/james-rodriguez-swim-coach",
        "years_experience": 15,
        "education": "BSc Sports Science (Loughborough University), ASA Level 2 Swimming Teaching Qualification",
        "certifications": "ASA Competitive Coach Level 2, National Pool Lifeguard, Sports Psychology Practitioner",
        "teaching_philosophy": "Swimming is not just about technique—it's about building confidence, resilience, and a lifelong love of being active. Every child can learn to swim safely and enjoy the water.",
        "bio": "Former professional footballer who now dedicates his time to youth development. James focuses on building confidence, teamwork, and physical fitness through engaging sports activities."
    },
    "Emily Thompson": {
        "linkedin_url": "https://linkedin.com/in/emily-thompson-creative-writer",
        "years_experience": 12,
        "education": "MA Creative Writing (University of East Anglia), BA English Literature (University of Oxford)",
        "certifications": "Published Author (3 novels), National Literacy Trust Workshop Leader",
        "teaching_philosophy": "Every child has a unique voice and story to tell. My role is to create a safe, inspiring space where young writers can explore their creativity without fear of judgment.",
        "bio": "Award-winning author with three published novels. Emily has run creative writing workshops in over 50 schools and believes passionately in nurturing the next generation of storytellers."
    },
    "David Park": {
        "linkedin_url": "https://linkedin.com/in/david-park-software-engineer",
        "years_experience": 10,
        "education": "BSc Computer Science (University of Cambridge), MSc Software Engineering (Imperial College London)",
        "certifications": "Google Certified Educator Level 2, Python Institute Certified Professional, Microsoft Innovative Educator",
        "teaching_philosophy": "Coding is the literacy of the 21st century. I teach students to think computationally and break down complex problems into manageable solutions.",
        "bio": "Senior software engineer who has worked at Google and Microsoft. David is passionate about making computer science accessible and exciting for young learners through game development and interactive projects."
    }
}

def update_tutors():
    with app.app_context():
        updated_count = 0
        
        for full_name, data in tutor_data.items():
            tutor = Tutor.query.filter_by(full_name=full_name).first()
            
            if tutor:
                print(f"\nUpdating {full_name}...")
                tutor.linkedin_url = data["linkedin_url"]
                tutor.years_experience = data["years_experience"]
                tutor.education = data["education"]
                tutor.certifications = data["certifications"]
                tutor.teaching_philosophy = data["teaching_philosophy"]
                tutor.bio = data["bio"]
                
                # Ensure status is approved
                if tutor.status != 'approved':
                    tutor.status = 'approved'
                    print(f"  - Set status to 'approved'")
                
                updated_count += 1
                print(f"  ✓ Updated successfully")
            else:
                print(f"\n⚠ Warning: Tutor '{full_name}' not found in database")
        
        # Commit all changes
        db.session.commit()
        print(f"\n{'='*60}")
        print(f"✓ Successfully updated {updated_count} tutor profiles")
        print(f"{'='*60}")
        
        # Display updated tutors
        print("\nVerifying updates:")
        all_tutors = Tutor.query.all()
        for tutor in all_tutors:
            print(f"\n{tutor.full_name} ({tutor.specialization})")
            print(f"  LinkedIn: {tutor.linkedin_url or 'Not set'}")
            print(f"  Experience: {tutor.years_experience or 'Not set'} years")
            print(f"  Status: {tutor.status}")

if __name__ == "__main__":
    print("="*60)
    print("TUTOR PROFILE UPDATE SCRIPT")
    print("="*60)
    update_tutors()
