"""
Simple verification script to check tutor profile data
"""
from app import app, db, Tutor

def verify_tutors():
    with app.app_context():
        tutors = Tutor.query.all()
        
        print("="*70)
        print(f"TUTOR PROFILE VERIFICATION - Found {len(tutors)} tutors")
        print("="*70)
        
        for tutor in tutors:
            print(f"\n📚 {tutor.full_name} - {tutor.specialization}")
            print(f"   Status: {tutor.status}")
            print(f"   LinkedIn: {tutor.linkedin_url or 'NOT SET'}")
            print(f"   Experience: {tutor.years_experience or 'NOT SET'} years")
            print(f"   Education: {(tutor.education[:50] + '...') if tutor.education else 'NOT SET'}")
            print(f"   Certifications: {(tutor.certifications[:50] + '...') if tutor.certifications else 'NOT SET'}")
            print(f"   Teaching Philosophy: {(tutor.teaching_philosophy[:50] + '...') if tutor.teaching_philosophy else 'NOT SET'}")
            print(f"   Bio: {(tutor.bio[:50] + '...') if tutor.bio else 'NOT SET'}")
        
        print("\n" + "="*70)
        
        # Check for any missing data
        missing_data = []
        for tutor in tutors:
            missing_fields = []
            if not tutor.linkedin_url: missing_fields.append("LinkedIn")
            if not tutor.years_experience: missing_fields.append("Experience")
            if not tutor.education: missing_fields.append("Education")
            if not tutor.teaching_philosophy: missing_fields.append("Teaching Philosophy")
            if not tutor.bio: missing_fields.append("Bio")
            
            if missing_fields:
                missing_data.append((tutor.full_name, missing_fields))
        
        if missing_data:
            print("\n⚠️  TUTORS WITH MISSING DATA:")
            for name, fields in missing_data:
                print(f"   - {name}: Missing {', '.join(fields)}")
        else:
            print("\n✅ ALL TUTORS HAVE COMPLETE PROFESSIONAL PROFILES!")
        
        print("="*70)

if __name__ == "__main__":
    verify_tutors()
