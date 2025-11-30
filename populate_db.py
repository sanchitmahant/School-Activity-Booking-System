"""
Quick database population script for demonstration
"""
from app import app, db, Admin, Tutor, Activity, Parent, Child

with app.app_context():
    print("🔄 Populating database with sample data...")
    
    # Create Admin
    admin = Admin(email='greenwoodinternationaluk@gmail.com')
    admin.set_password('sanchitkaushal')
    db.session.add(admin)
    
    # Create Professional Tutors with Bios
    tutors_data = [
        {
            'full_name': 'Dr. Sarah Jenkins',
            'email': 'drjenkins.greenwood@gmail.com',
            'specialization': 'Robotics & Engineering',
            'qualifications': 'PhD in Robotics Engineering (MIT), MEng in Mechanical Engineering (Imperial College London)',
            'bio': 'Dr. Jenkins has over 15 years of experience in robotics education and has led numerous award-winning student teams to national competitions. She specializes in making complex engineering concepts accessible to young learners.'
        },
        {
            'full_name': 'Prof. Michael Chen',
            'email': 'michael.chen@greenwood.edu.uk',
            'specialization': 'Computer Science & Programming',
            'qualifications': 'PhD in Computer Science (Stanford), BSc in Software Engineering (Cambridge)',
            'bio': 'Professor Chen is a former Google software engineer with a passion for teaching young people to code. He has developed innovative curriculum for teaching Python and web development to students of all ages.'
        },
        {
            'full_name': 'Emma Thompson',
            'email': 'emma.thompson@greenwood.edu.uk',
            'specialization': 'Visual Arts & Design',
            'qualifications': 'MA in Fine Arts (Royal College of Art), BA in Art History (Oxford)',
            'bio': 'Emma is an accomplished artist whose work has been exhibited in galleries across Europe. She brings creativity and professional techniques to her teaching, helping students develop their artistic voice and technical skills.'
        },
        {
            'full_name': 'James Rodriguez',
            'email': 'james.rodriguez@greenwood.edu.uk',
            'specialization': 'Sports & Physical Education',
            'qualifications': 'MSc in Sports Science (Loughborough), Level 3 Personal Training, FA Coaching Badge',
            'bio': 'James is a former professional footballer who now dedicates his time to youth development. He focuses on building confidence, teamwork, and physical fitness through engaging sports activities.'
        },
        {
            'full_name': 'Dr. Amelia Watson',
            'email': 'amelia.watson@greenwood.edu.uk',
            'specialization': 'Music & Performance',
            'qualifications': 'DMA in Music Performance (Juilliard), ABRSM Diploma, Grade 8 Piano & Violin',
            'bio': 'Dr. Watson is a concert pianist and music educator with 20 years of experience. She creates a nurturing environment where students can explore their musical talents and develop performance confidence.'
        },
        {
            'full_name': 'David Park',
            'email': 'david.park@greenwood.edu.uk',
            'specialization': 'Drama & Theatre',
            'qualifications': 'MA in Theatre Arts (RADA), BA in Performing Arts (LAMDA)',
            'bio': 'David is a professional actor and director who has worked in West End productions. He helps students build confidence, creativity, and communication skills through engaging drama workshops and performances.'
        }
    ]
    
    tutors = []
    for t_data in tutors_data:
        tutor = Tutor(
            full_name=t_data['full_name'],
            email=t_data['email'],
            specialization=t_data['specialization'],
            qualifications=t_data['qualifications'],
            bio=t_data['bio'],
            photo_url='default-avatar.png'  # Can be updated later
        )
        tutor.set_password('tutor123')
        db.session.add(tutor)
        tutors.append(tutor)
    
    db.session.commit()
    print(f"✅ Created {len(tutors)} tutors")
    
    # Create Activities with detailed descriptions
    activities_data = [
        {
            'name': 'Robotics Club',
            'description': 'Dive into the exciting world of robotics! Students will learn to design, build, and program robots using LEGO Mindstorms and Arduino platforms. This hands-on club covers mechanical design, sensors, motors, and basic programming. Perfect for budding engineers who love to create and problem-solve.',
            'price': 50.00,
            'tutor': tutors[0],  # Dr. Sarah Jenkins
            'day': 'Monday',
            'start': '15:00',
            'end': '16:30',
            'capacity': 20
        },
        {
            'name': 'Swimming',
            'description': 'Professional swimming instruction for all levels from beginners to advanced. Students will develop water confidence, learn proper stroke techniques (freestyle, backstroke, breaststroke, butterfly), and improve their overall fitness. Certified lifeguards always present for safety.',
            'price': 30.00,
            'tutor': tutors[3],  # James Rodriguez
            'day': 'Tuesday',
            'start': '15:00',
            'end': '16:30',
            'capacity': 15
        },
        {
            'name': 'Creative Writing Workshop',
            'description': 'Unleash your imagination through creative writing! This workshop covers storytelling techniques, character development, poetry, and creative expression. Students will explore various writing styles and genres while developing their unique voice. Each session includes writing exercises, peer review, and individual feedback.',
            'price': 25.00,
            'tutor': tutors[2],  # Emma Thompson
            'day': 'Wednesday',
            'start': '14:00',
            'end': '15:30',
            'capacity': 18
        },
        {
            'name': 'Python Programming',
            'description': 'Learn to code with Python, one of the most popular programming languages! Students will master fundamental concepts including variables, loops, functions, and object-oriented programming. Projects include game development, data analysis, and web scraping. No prior experience needed!',
            'price': 45.00,
            'tutor': tutors[1],  # Prof. Michael Chen
            'day': 'Thursday',
            'start': '15:30',
            'end': '17:00',
            'capacity': 20
        },
        {
            'name': 'Art & Design Studio',
            'description': 'Explore various artistic mediums including drawing, painting, sculpture, and digital art. Students will learn professional techniques, color theory, composition, and art history while developing their creative portfolio. All materials provided. Suitable for all skill levels.',
            'price': 35.00,
            'tutor': tutors[2],  # Emma Thompson
            'day': 'Friday',
            'start': '14:30',
            'end': '16:00',
            'capacity': 16
        },
        {
            'name': 'Drama & Performance',
            'description': 'Build confidence and creativity through drama! Students will learn acting techniques, improvisation, voice projection, and stage presence. The club culminates in a end-of-term performance for parents. Develops public speaking, teamwork, and self-expression skills.',
            'price': 40.00,
            'tutor': tutors[5],  # David Park
            'day': 'Monday',
            'start': '16:00',
            'end': '17:30',
            'capacity': 20
        },
        {
            'name': 'Music Ensemble',
            'description': 'Join our musical ensemble to develop performance skills in a collaborative environment. Students will learn ensemble playing, music theory, sight-reading, and performance techniques. Instruments include piano, strings, and vocals. Regular concerts and performances scheduled.',
            'price': 38.00,
            'tutor': tutors[4],  # Dr. Amelia Watson
            'day': 'Wednesday',
            'start': '16:00',
            'end': '17:30',
            'capacity': 25
        },
        {
            'name': 'Football Skills Academy',
            'description': 'Develop football skills with professional coaching! Focus on ball control, passing, shooting, tactical awareness, and teamwork. Students participate in drills, small-sided games, and fitness training. All equipment provided. Both recreational and competitive pathways available.',
            'price': 32.00,
            'tutor': tutors[3],  # James Rodriguez
            'day': 'Friday',
            'start': '15:00',
            'end': '16:30',
            'capacity': 24
        }
    ]
    
    for a_data in activities_data:
        activity = Activity(
            name=a_data['name'],
            description=a_data['description'],
            price=a_data['price'],
            tutor_id=a_data['tutor'].id,
            day_of_week=a_data['day'],
            start_time=a_data['start'],
            end_time=a_data['end'],
            max_capacity=a_data['capacity']
        )
        db.session.add(activity)
    
    db.session.commit()
    print(f"✅ Created {len(activities_data)} activities")
    
    # Create Demo Parent Account
    parent = Parent(
        email='parent@demo.com',
        full_name='Demo Parent',
        phone='07123456789'
    )
    parent.set_password('demo123')
    db.session.add(parent)
    db.session.commit()
    
    # Create Demo Child
    child = Child(
        parent_id=parent.id,
        name='Alex Johnson',
        age=10,
        grade='5'
    )
    db.session.add(child)
    db.session.commit()
    
    print("✅ Created demo parent and child")
    print("\n🎉 Database populated successfully!")
    print("\n📝 Login Credentials:")
    print("   Admin: greenwoodinternationaluk@gmail.com / sanchitkaushal")
    print("   Parent: parent@demo.com / demo123")
    print("   Tutors: [tutor-email] / tutor123")
    print("\n✨ System ready for demonstration!")
