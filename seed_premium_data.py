"""
Premium Activities & Tutors Database Seeder
Creates world-class activities with elite tutors for Greenwood International School
"""
from app import app, db, Admin, Tutor, Activity
from datetime import datetime

def seed_premium_activities():
    """Seed database with premium activities and elite tutors"""
    
    with app.app_context():
        print("🎓 Seeding Greenwood International School with Premium Content...")
        
        # Elite Tutors with Professional Credentials
        tutors_data = [
            {
                'email': 'dr.richardson@greenwood.edu',
                'full_name': 'Dr. James Richardson',
                'specialization': 'Classical Piano & Music Theory',
                'qualification': 'PhD in Music Performance, Royal Academy of Music',
                'bio': 'Concert pianist with 20+ years performing at Carnegie Hall and Royal Albert Hall',
                'years_experience': 25,
                'education': 'PhD Music Performance (Royal Academy), MMus (Juilliard)',
                'linkedin_url': 'https://linkedin.com/in/jamesrichardson',
                'certifications': 'ABRSM Diploma, Trinity College London Fellow'
            },
            {
                'email': 'prof.martinez@greenwood.edu',
                'full_name': 'Professor Elena Martinez',
                'specialization': 'Advanced Mathematics & Olympiad Preparation',
                'qualification': 'PhD Mathematics, Cambridge University',
                'bio': 'Former IMO gold medalist, specializing in gifted student development',
                'years_experience': 18,
                'education': 'PhD Mathematics (Cambridge), MSc Pure Mathematics (MIT)',
                'linkedin_url': 'https://linkedin.com/in/elenamartinez',
                'certifications': 'IMO Coach Certification, Cambridge Examiner'
            },
            {
                'email': 'coach.williams@greenwood.edu',
                'full_name': 'Coach Marcus Williams',
                'specialization': 'Elite Tennis & Athletic Development',
                'qualification': 'Former ATP Professional, Level 5 LTA Coach',
                'bio': 'Trained 15 national champions, former Wimbledon quarter-finalist',
                'years_experience': 22,
                'education': 'BSc Sports Science (Loughborough), ATP Professional Certification',
                'linkedin_url': 'https://linkedin.com/in/marcuswilliams',
                'certifications': 'LTA Level 5, USTA High Performance, Sports Psychology Diploma'
            },
            {
                'email': 'dr.chen@greenwood.edu',
                'full_name': 'Dr. Mei Chen',
                'specialization': 'Mandarin Language & Chinese Culture',
                'qualification': 'PhD Chinese Linguistics, Beijing University',
                'bio': 'Native speaker with expertise in HSK preparation and cultural immersion',
                'years_experience': 15,
                'education': 'PhD Chinese Linguistics (Beijing Univ), MA Teaching Chinese as Foreign Language',
                'linkedin_url': 'https://linkedin.com/in/meichen',
                'certifications': 'HSK Examiner, Confucius Institute Certified, IB Chinese Certified'
            },
            {
                'email': 'prof.blackwood@greenwood.edu',
                'full_name': 'Professor Alexander Blackwood',
                'specialization': 'Advanced Robotics & AI Programming',
                'qualification': 'PhD Artificial Intelligence, Stanford University',
                'bio': 'Former Google AI researcher, FTC Robotics Championship coach',
                'years_experience': 12,
                'education': 'PhD AI (Stanford), MSc Computer Science (MIT)',
                'linkedin_url': 'https://linkedin.com/in/alexanderblackwood',
                'certifications': 'FIRST Robotics Mentor, Python Institute Certified, AWS ML Specialist'
            },
            {
                'email': 'ms.laurent@greenwood.edu',
                'full_name': 'Mademoiselle Sophie Laurent',
                'specialization': 'French Language & European Literature',
                'qualification': 'Agrégation de Lettres Modernes, Sorbonne University',
                'bio': 'Native Parisian, specializing in DELF/DALF and IB French preparation',
                'years_experience': 14,
                'education': 'Agrégation (Sorbonne), MA French Literature (École Normale Supérieure)',
                'linkedin_url': 'https://linkedin.com/in/sophielaurent',
                'certifications': 'DELF/DALF Examiner, IB French HL Examiner, Alliance Française Certified'
            },
            {
                'email': 'maestro.rossi@greenwood.edu',
                'full_name': 'Maestro Giovanni Rossi',
                'specialization': 'Classical Violin & Chamber Music',
                'qualification': 'Master of Music, Conservatorio di Santa Cecilia',
                'bio': 'Principal violinist with London Symphony Orchestra, chamber music specialist',
                'years_experience': 28,
                'education': 'MMus (Santa Cecilia Rome), Performance Diploma (Salzburg Mozarteum)',
                'linkedin_url': 'https://linkedin.com/in/giovannirossi',
                'certifications': 'ABRSM Diploma, Suzuki Method Certified'
            },
            {
                'email': 'dr.patel@greenwood.edu',
                'full_name': 'Dr. Priya Patel',
                'specialization': 'Experimental Science & Research Methods',
                'qualification': 'PhD Biochemistry, Oxford University',
                'bio': 'Published researcher with expertise in science olympiad preparation',
                'years_experience': 16,
                'education': 'PhD Biochemistry (Oxford), MSc Molecular Biology (Imperial College)',
                'linkedin_url': 'https://linkedin.com/in/priyapatel',
                'certifications': 'Science Olympiad Coach, CREST Award Assessor, IB Science Examiner'
            },
            {
                'email': 'sir.thompson@greenwood.edu',
                'full_name': 'Sir Geoffrey Thompson',
                'specialization': 'English Literature & Creative Writing',
                'qualification': 'DPhil English Literature, University of Oxford',
                'bio': 'Published novelist and poet, former Oxford tutorial fellow',
                'years_experience': 30,
                'education': 'DPhil English Lit (Oxford), MA Creative Writing (UEA)',
                'linkedin_url': 'https://linkedin.com/in/geoffreythompson',
                'certifications': 'A-Level Examiner (AQA), IB English Examiner, Royal Society of Literature Fellow'
            },
            {
                'email': 'coach.anderson@greenwood.edu',
                'full_name': 'Coach Sarah Anderson',
                'specialization': 'Competitive Swimming & Triathlon',
                'qualification': 'Olympic Swimming Coach Level 4, ASA',
                'bio': 'Former Olympic swimmer, trained 8 national record holders',
                'years_experience': 19,
                'education': 'BSc Sports Science (Bath), ASA Level 4 Coaching',
                'linkedin_url': 'https://linkedin.com/in/sarahanderson',
                'certifications': 'ASA Level 4, Triathlon England Coach, Sports Psychology Certified'
            },
            {
                'email': 'ms.nakamura@greenwood.edu',
                'full_name': 'Ms. Yuki Nakamura',
                'specialization': 'Contemporary Art & Digital Design',
                'qualification': 'MFA Fine Arts, Royal College of Art',
                'bio': 'Award-winning digital artist with exhibitions at Tate Modern',
                'years_experience': 13,
                'education': 'MFA (Royal College of Art), BA Fine Arts (Tokyo University of Arts)',
                'linkedin_url': 'https://linkedin.com/in/yukinakamura',
                'certifications': 'Adobe Certified Professional, IB Visual Arts Examiner'
            },
            {
                'email': 'prof.oconnor@greenwood.edu',
                'full_name': 'Professor Liam O\'Connor',
                'specialization': 'Classical Guitar & Music Composition',
                'qualification': 'DMus Performance, Guildhall School of Music',
                'bio': 'International concert guitarist, composer for film and theatre',
                'years_experience': 21,
                'education': 'DMus Performance (Guildhall), MMus Composition (Royal Northern)',
                'linkedin_url': 'https://linkedin.com/in/liamoconnor',
                'certifications': 'Trinity College London Fellow, ABRSM Diploma'
            }
        ]
        
        # Create tutors
        created_tutors = {}
        for tutor_data in tutors_data:
            tutor = Tutor.query.filter_by(email=tutor_data['email']).first()
            if not tutor:
                tutor = Tutor(
                    email=tutor_data['email'],
                    full_name=tutor_data['full_name'],
                    specialization=tutor_data['specialization'],
                    qualification=tutor_data['qualification'],
                    bio=tutor_data['bio'],
                    years_experience=tutor_data['years_experience'],
                    education=tutor_data['education'],
                    linkedin_url=tutor_data['linkedin_url'],
                    certifications=tutor_data['certifications']
                )
                tutor.set_password('change_me')  # Change in production
                db.session.add(tutor)
                print(f"✅ Created tutor: {tutor_data['full_name']}")
            created_tutors[tutor_data['email']] = tutor
        
        db.session.commit()
        
        # Premium Activities
        activities_data = [
            # Music & Performing Arts
            {'name': 'Concert Piano Masterclass', 'tutor_email': 'dr.richardson@greenwood.edu', 
             'day': 'Monday', 'time': '16:00-17:30', 'price': 85.00, 'capacity': 6,
             'description': 'Individual and small group instruction for advanced pianists preparing for conservatory auditions or international competitions.'},
            
            {'name': 'Classical Violin Ensemble', 'tutor_email': 'maestro.rossi@greenwood.edu',
             'day': 'Tuesday', 'time': '15:30-17:00', 'price': 75.00, 'capacity': 8,
             'description': 'Chamber music training with professional performance opportunities at prestigious venues.'},
            
            {'name': 'Classical Guitar & Composition', 'tutor_email': 'prof.oconnor@greenwood.edu',
             'day': 'Thursday', 'time': '16:00-17:30', 'price': 70.00, 'capacity': 8,
             'description': 'Technical mastery and creative composition for classical guitar students.'},
            
            # Academic Excellence
            {'name': 'Mathematics Olympiad Preparation', 'tutor_email': 'prof.martinez@greenwood.edu',
             'day': 'Wednesday', 'time': '16:30-18:00', 'price': 80.00, 'capacity': 10,
             'description': 'Advanced problem-solving for IMO, UKMT, and university entrance competitions.'},
            
            {'name': 'Experimental Science Lab', 'tutor_email': 'dr.patel@greenwood.edu',
             'day': 'Friday', 'time': '15:00-17:00', 'price': 75.00, 'capacity': 12,
             'description': 'Hands-on research methods, lab techniques, and science olympiad preparation with cutting-edge equipment.'},
            
            {'name': 'Creative Writing Workshop', 'tutor_email': 'sir.thompson@greenwood.edu',
             'day': 'Monday', 'time': '15:30-17:00', 'price': 65.00, 'capacity': 12,
             'description': 'Literary analysis and creative composition with a published author and Oxford fellow.'},
            
            # Languages & Culture
            {'name': 'Advanced Mandarin & Chinese Culture', 'tutor_email': 'dr.chen@greenwood.edu',
             'day': 'Tuesday', 'time': '16:00-17:30', 'price': 70.00, 'capacity': 10,
             'description': 'HSK preparation, classical literature, and cultural immersion with native expertise.'},
            
            {'name': 'French Language & Literature', 'tutor_email': 'ms.laurent@greenwood.edu',
             'day': 'Thursday', 'time': '15:30-17:00', 'price': 68.00, 'capacity': 10,
             'description': 'DELF/DALF preparation and French literary classics with Sorbonne-trained instructor.'},
            
            # Technology & Innovation
            {'name': 'Advanced Robotics & AI Programming', 'tutor_email': 'prof.blackwood@greenwood.edu',
             'day': 'Wednesday', 'time': '15:00-17:00', 'price': 90.00, 'capacity': 12,
             'description': 'Machine learning, robotics competitions, and real-world AI applications with Stanford PhD.'},
            
            # Athletics & Wellness
            {'name': 'Elite Tennis Development', 'tutor_email': 'coach.williams@greenwood.edu',
             'day': 'Monday', 'time': '16:00-18:00', 'price': 95.00, 'capacity': 8,
             'description': 'Professional-level coaching for competitive tennis with former ATP player.'},
            
            {'name': 'Competitive Swimming Squad', 'tutor_email': 'coach.anderson@greenwood.edu',
             'day': 'Tuesday', 'time': '16:30-18:00', 'price': 85.00, 'capacity': 15,
             'description': 'Olympic-standard training for national and regional championships.'},
            
            # Arts & Design
            {'name': 'Contemporary Art & Digital Design', 'tutor_email': 'ms.nakamura@greenwood.edu',
             'day': 'Friday', 'time': '15:30-17:30', 'price': 72.00, 'capacity': 10,
             'description': 'Mixed media, digital art, and portfolio development for art school applications.'},
            
            # Additional Premium Offerings
            {'name': 'Junior Concert Piano', 'tutor_email': 'dr.richardson@greenwood.edu',
             'day': 'Thursday', 'time': '15:00-16:00', 'price': 60.00, 'capacity': 8,
             'description': 'Foundation piano skills for younger students (Ages 7-11) with Royal Academy expertise.'},
            
            {'name': 'Science Research Club', 'tutor_email': 'dr.patel@greenwood.edu',
             'day': 'Monday', 'time': '16:30-17:30', 'price': 55.00, 'capacity': 15,
             'description': 'Independent research projects and academic publication preparation.'},
            
            {'name': 'Tennis Fundamentals', 'tutor_email': 'coach.williams@greenwood.edu',
             'day': 'Friday', 'time': '15:00-16:30', 'price': 58.00, 'capacity': 12,
             'description': 'Technical foundation for beginner and intermediate players.'},
            
            {'name': 'Mandarin for Beginners', 'tutor_email': 'dr.chen@greenwood.edu',
             'day': 'Wednesday', 'time': '15:30-16:30', 'price': 50.00, 'capacity': 15,
             'description': 'Introduction to Mandarin language and culture for young learners.'},
            
            {'name': 'Creative Writing Clinic', 'tutor_email': 'sir.thompson@greenwood.edu',
             'day': 'Friday', 'time': '16:00-17:00', 'price': 48.00, 'capacity': 15,
             'description': 'Story crafting, poetry, and expressive writing for all levels.'},
            
            {'name': 'French Conversation Circle', 'tutor_email': 'ms.laurent@greenwood.edu',
             'day': 'Monday', 'time': '15:00-16:00', 'price': 45.00, 'capacity': 12,
             'description': 'Immersive conversation practice with native Parisian instructor.'},
            
            {'name': 'Robotics Beginners Workshop', 'tutor_email': 'prof.blackwood@greenwood.edu',
             'day': 'Saturday', 'time': '10:00-12:00', 'price': 65.00, 'capacity': 16,
             'description': 'Introduction to coding, engineering, and robot construction for young minds.'},
            
            {'name': 'Young Artists Studio', 'tutor_email': 'ms.nakamura@greenwood.edu',
             'day': 'Wednesday', 'time': '15:00-16:30', 'price': 52.00, 'capacity': 12,
             'description': 'Painting, drawing, and creative exploration for developing artists.'},
        ]
        
        # Create activities
        for act_data in activities_data:
            activity = Activity.query.filter_by(name=act_data['name']).first()
            if not activity:
                tutor = created_tutors.get(act_data['tutor_email'])
                activity = Activity(
                    name=act_data['name'],
                    day_of_week=act_data['day'],
                    start_time=act_data['time'].split('-')[0],
                    end_time=act_data['time'].split('-')[1],
                    cost=act_data['price'],
                    capacity=act_data['capacity'],
                    description=act_data['description'],
                    location='Greenwood International School',
                    tutor_id=tutor.id if tutor else None
                 )
                db.session.add(activity)
                print(f"✅ Created activity: {act_data['name']} - £{act_data['price']}")
        
        db.session.commit()
        print(f"\n🎉 Successfully seeded {len(activities_data)} premium activities with {len(tutors_data)} elite tutors!")
        print("💎 Greenwood International School is now truly world-class!")

if __name__ == '__main__':
    seed_premium_activities()
