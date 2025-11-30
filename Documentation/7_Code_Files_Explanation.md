# Code Files Explanation
**Project**: School Activity Booking System  
**Total Files**: 50+  
**Lines of Code**: 3,200+

---

## PART 1: SIMPLE FILE OVERVIEW

### Project Structure (Like a House)

```
School_Activity_Booking_System/
│
├── app.py                    ← The BRAIN (main logic)
├── config.py                 ← The SETTINGS (configuration)
├── requirements.txt          ← The SHOPPING LIST (dependencies)
├── Procfile                  ← The INSTRUCTIONS (for deployment)
│
├── templates/                ← The PAGES (HTML files)
│   ├── base.html            ← The TEMPLATE (all pages use this)
│   ├── login.html           ← Parent login page
│   ├── dashboard.html       ← Parent home page
│   ├── admin/               ← Admin pages folder
│   └── tutor/               ← Tutor pages folder
│
├── static/                   ← The DECORATION (CSS, images, JS)
│   ├── css/style.css        ← The PAINT (styling)
│   ├── js/script.js         ← The MAGIC (JavaScript)
│   └── images/              ← The PICTURES
│
├── Documentation/            ← The MANUAL (user guides)
└── helpers/                   ← The TOOLS (utility scripts)
```

---

## PART 2: CORE FILES EXPLAINED

### 1. app.py - The Brain (1,300 lines)

**Simple Explanation:**
This is the main file - like your brain controls your body, app.py controls the whole website!

**What's Inside:**

**Lines 1-50: Imports (Getting Tools)**
```python
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
# Like gathering all your cooking utensils before starting
```

**Lines 50-350: Database Models (Defining Things)**
```python
class Parent(db.Model):
    # This defines what a "Parent" is
    # Like a form: "Parent has name, email, phone"
    
class Child(db.Model):
    # What is a "Child"?
    # Has name, age, grade, belongs to a parent
```

**Lines 350-600: Helper Functions (Tools)**
```python
def send_email(recipient, subject, body):
    # Tool for sending emails
    
def generate_pdf(booking):
    # Tool for making PDF invoices
```

**Lines 600-1300: Routes (The Pages)**
```python
@app.route('/login')
def login():
    # What happens when you visit /login
    
@app.route('/dashboard')
def dashboard  ():
    # What happens when you visit /dashboard
```

**Technical Breakdown:**

| Section | Lines | Purpose | Contributor |
|---------|-------|---------|-------------|
| Imports | 1-50 | Dependencies | All |
| Configuration | 51-80 | App setup | Sanchit |
| Database Models | 81-350 | ORM definitions | Shiva |
| Security Functions | 351-450 | Auth/CSRF | Sanchit |
| Email Functions | 451-550 | SMTP/Templates | Chichebendu |
| PDF Functions | 551-650 | ReportLab | Chichebendu |
| Parent Routes | 651-850 | Parent portal | All |
| Admin Routes | 851-1050 | Admin CRUD | Sanchit |
| Tutor Routes | 1051-1250 | Tutor portal | Chichebendu |
| Helper Routes | 1251-1300 | API endpoints | Mohd |

---

### 2. config.py - The Settings (70 lines)

**Simple Explanation:**
Like the settings menu on your phone - controls how the app works in different situations!

**What's Inside:**

```python
class Config:
    # Basic settings everyone uses
    SECRET_KEY = "super-secret-password"
    
class DevelopmentConfig(Config):
    # Settings for testing on your computer
    DEBUG = True  # Show errors
    DATABASE = "test.db"  # Small test database
    
class ProductionConfig(Config):
    # Settings for real users on internet
    DEBUG = False  # Hide errors from users
    DATABASE = "real-database.postgresql"  # Big real database
```

**Technical Details:**

```python
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32).hex()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

class DevelopmentConfig(Config):
    """Development settings"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True  # Log all SQL queries
    MAIL_DEBUG = True
    
class ProductionConfig(Config):
    """Production settings"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW = 40
```

**Contributor:** Sanchit (Configuration architecture)

---

### 3. templates/ - The HTML Pages (18 files)

**Simple Explanation:**
These are the web pages you see! Like different rooms in a house.

**Base Template (base.html):**
```html
<!-- The foundation all pages build on -->
<!DOCTYPE html>
<html>
<head>
    <title>School Booking</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <!-- Navigation bar (on every page) -->
    <nav>...</nav>
    
    <!-- Content (changes per page) -->
    {% block content %}{% endblock %}
    
    <!-- Footer (on every page) -->
    <footer>...</footer>
</body>
</html>
```

**All Templates:**

**Parent Portal (5 files):**
1. `login.html` - Login page (email + password form)
2. `register.html` - Sign up page (create account)
3. `dashboard.html` - Home page (see your bookings)
4. `activities.html` - Browse activities (swimming, art, etc.)
5. `booking_success.html` - Confirmation page (booking confirmed!)

**Admin Portal (6 files):**
1. `admin/login.html` - Admin login
2. `admin/dashboard.html` - Statistics dashboard
3. `admin/activities.html` - Manage activities list
4. `admin/create_activity.html` - Add new activity form
5. `admin/edit_activity.html` - Edit activity details
6. `admin/bookings.html` - View all bookings

**Tutor Portal (4 files):**
1. `tutor/login.html` - Tutor login
2. `tutor/dashboard.html` - Tutor home (their activities)
3. `tutor/attendance.html` - Mark attendance form
4. `tutor/attendance_history.html` - View past attendance

**General (3 files):**
1. `base.html` - Template foundation
2. `index.html` - Homepage (public, before login)
3. `error.html` - Error page (404, 500)

**Technical Details - Template Inheritance:**

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}School Booking{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- dashboard.html extends base -->
{% extends "base.html" %}

{% block title %}Parent Dashboard{% endblock %}

{% block content %}
    <h1>Welcome, {{ parent.full_name }}!</h1>
    <!-- Dashboard content -->
{% endblock %}
```

**Contributors:**
- Parent templates: All team members
- Admin templates: Sanchit
- Tutor templates: Chichebendu

---

### 4. static/css/style.css - The Styling (500 lines)

**Simple Explanation:**
Makes the website look pretty! Like interior design for web pages.

**What's Inside:**

```css
/* Colors and Fonts */
:root {
    --primary-color: #667eea;     /* Purple */
    --secondary-color: #764ba2;    /* Dark purple */
    --success-color: #10b981;      /* Green */
    --danger-color: #ef4444;       /* Red */
}

/* Buttons */
.btn {
    padding: 12px 24px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
}

.btn:hover {
    transform: scale(1.05);  /* Grow slightly on hover */
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

/* Cards */
.activity-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

**Structure:**

| Section | Lines | Purpose |
|---------|-------|---------|
| CSS Variables | 1-30 | Colors, fonts |
| Reset Styles | 31-60 | Browser defaults |
| Layout | 61-150 | Grid, flexbox |
| Components | 151-300 | Buttons, cards, forms |
| Utilities | 301-400 | Spacing, colors |
| Animations | 401-500 | Transitions, keyframes |

**Contributor:** Team effort (design decisions by all)

---

### 5. static/js/script.js - The JavaScript (400 lines)

**Simple Explanation:**
Makes the website interactive! Like adding motion sensors and automatic doors.

**What's Inside:**

```javascript
// AJAX Delete (Delete without page reload)
function deleteActivity(id) {
    if (!confirm('Are you sure?')) return;
    
    fetch(`/admin/delete_activity/${id}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove from page smoothly
            document.getElementById(`activity-${id}`).remove();
            showNotification('Deleted successfully!');
        }
    });
}

// Lazy Image Loading
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.src = entry.target.dataset.src;
        }
    });
});

// Form Validation
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}
```

**Structure:**

| Section | Lines | Purpose | Contributor |
|---------|-------|---------|-------------|
| AJAX Functions | 1-150 | Async requests | Mohd |
| Lazy Loading | 151-200 | Image optimization | Mohd |
| Form Validation | 201-280 | Client validation | Mohd |
| UI Helpers | 281-350 | Notifications, modals | Mohd |
| Cache Manager | 351-400 | LocalStorage | Mohd |

---

### 6. Helper Scripts (5 files)

**populate_db.py (200 lines)**

**Simple Explanation:**
Creates fake demo data for testing. Like putting mannequins in a store before it opens!

```python
# Creates:
admin = Admin(email='admin@greenwood.com', password='admin123')
parent = Parent(email='john@email.com', full_name='John Smith')
child = Child(name='Emma', age=8, grade=3, parent_id=parent.id)
tutor = Tutor(full_name='Dr. Sarah Jenkins', specialization='Swimming')
activity = Activity(name='Swimming Lessons', price=25.00, max_capacity=15)

# Result: Complete test database ready to use!
```

**Technical Implementation:**

```python
from app import app, db, Parent, Child, Activity, Tutor, Admin, Booking
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def populate_database():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    # Create admin
    admin = Admin(
        email='admin@greenwood.com',
        full_name='System Administrator',
        password_hash=generate_password_hash('admin123')
    )
    db.session.add(admin)
    
    # Create parent + children
    parent = Parent(
        email='john.smith@email.com',
        full_name='John Smith',
        phone='07123456789',
        password_hash=generate_password_hash('password123')
    )
    db.session.add(parent)
    db.session.commit()  # Commit to get parent.id
    
    child1 = Child(
        name='Emma Smith',
        age=8,
        grade=3,
        parent_id=parent.id
    )
    child2 = Child(
        name='Oliver Smith',
        age=11,
        grade=6,
        parent_id=parent.id
    )
    db.session.add_all([child1, child2])
    
    # Create 6 tutors with specializations
    tutors_data = [
        ('Dr. Sarah Jenkins', 'Swimming', 'sarah.jenkins@greenwood.com'),
        ('Mr. David Chen', 'Art', 'david.chen@greenwood.com'),
        ('Ms. Emily Brown', 'Music', 'emily.brown@greenwood.com'),
        ('Mr. James Wilson', 'Coding', 'james.wilson@greenwood.com'),
        ('Ms. Lisa Taylor', 'Drama', 'lisa.taylor@greenwood.com'),
        ('Mr. Ahmed Khan', 'Sports', 'ahmed.khan@greenwood.com')
    ]
    
    tutors = []
    for name, spec, email in tutors_data:
        tutor = Tutor(
            full_name=name,
            email=email,
            specialization=spec,
            password_hash=generate_password_hash('tutor123')
        )
        tutors.append(tutor)
    db.session.add_all(tutors)
    db.session.commit()
    
    # Create 8 activities
    activities_data = [
        ('Swimming Lessons', 'Beginner swimming for ages 6-8', 25.00, 15, 0, 'Monday', '15:00', '16:00'),
        ('Art Class', 'Creative painting and drawing', 20.00, 12, 1, 'Tuesday', '14:00', '15:30'),
        ('Music Lessons', 'Piano and guitar basics', 30.00, 8, 2, 'Wednesday', '16:00', '17:00'),
        ('Coding Club', 'Python programming for kids', 35.00, 10, 3, 'Thursday', '15:30', '17:00'),
        ('Drama Workshop', 'Acting and stage performance', 22.00, 20, 4, 'Friday', '14:00', '16:00'),
        ('Football Training', 'Team sports and fitness', 18.00, 25, 5, 'Monday', '16:00', '17:30'),
        ('Chess Club', 'Strategic thinking and chess', 15.00, 16, 3, 'Tuesday', '15:00', '16:00'),
        ('Dance Class', 'Ballet and contemporary dance', 28.00, 14, 2, 'Wednesday', '14:30', '16:00')
    ]
    
    for name, desc, price, capacity, tutor_idx, day, start, end in activities_data:
        activity = Activity(
            name=name,
            description=desc,
            price=price,
            max_capacity=capacity,
            tutor_id=tutors[tutor_idx].id,
            day_of_week=day,
            start_time=start,
            end_time=end
        )
        db.session.add(activity)
    
    db.session.commit()
    print("✅ Database populated successfully!")
    print(f"   - Created 1 admin")
    print(f"   - Created 1 parent with 2 children")
    print(f"   - Created 6 tutors")
    print(f"   - Created 8 activities")

if __name__ == '__main__':
    with app.app_context():
        populate_database()
```

**Contributor:** Shiva (data generation)

---

**convert_to_pdf.py (80 lines)**

**Simple Explanation:**
Converts markdown documentation to PDF files. Like a printer that reads .md files!

```python
# Finds all .md files in Documentation/
# Converts each to PDF
# Saves in same folder

# Example:
# 1_Sanchit_Contribution.md → 1_Sanchit_Contribution.pdf
```

**Contributor:** Chichebendu (PDF utilities)

---

## PART 3: DATABASE FILES

**school_booking.db**

**Simple Explanation:**
The filing cabinet where all data is stored! Every parent, child, booking - everything!

**Structure (SQLite):**

```
Tables:
├── parent (stores parent accounts)
├── child (stores children info)
├── activity (stores available activities)
├── tutor (stores tutor accounts)
├── booking (stores all bookings)
├── waitlist (stores queue when full)
├── attendance (stores attendance records)
└── admin (stores admin accounts)

Size: ~5MB with sample data
Records: ~100 sample records
```

**Technical Schema:**

```sql
-- Example table structure
CREATE TABLE parent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_parent_email ON parent(email);

CREATE TABLE booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER NOT NULL,
    child_id INTEGER NOT NULL,
    activity_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    payment_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES parent(id),
    FOREIGN KEY (child_id) REFERENCES child(id),
    FOREIGN KEY (activity_id) REFERENCES activity(id),
    UNIQUE(child_id, activity_id, date)
);

CREATE INDEX idx_booking_status ON booking(status);
CREATE INDEX idx_booking_date ON booking(date);
```

**Contributor:** Shiva (schema design)

---

## PART 4: CONFIGURATION FILES

**requirements.txt**

**Simple Explanation:**
Shopping list of Python packages needed. Like ingredients list for a recipe!

```txt
Flask==2.3.0              # Web framework
Flask-SQLAlchemy==3.0.5   # Database
Flask-Mail==0.9.1         # Email
Flask-WTF==1.1.1          # Forms + CSRF
ReportLab==4.0.4          # PDF generation
Werkzeug==2.3.0           # Security utilities
python-dotenv==1.0.0      # Environment variables
gunicorn==21.2.0          # Production server
psycopg2-binary==2.9.9    # PostgreSQL
email-validator==2.0.0     # Email validation
WTForms==3.0.1            # Form validation
SQLAlchemy==2.0.20        # ORM core
```

**Contributors:** All team members

---

**Procfile**

**Simple Explanation:**
Instructions for deployment server on how to run the app!

```
web: gunicorn --workers 4 --threads 2 --timeout 120 --bind 0.0.0.0:$PORT app:app
```

**Translation:**
- `web:` - This is a web application
- `gunicorn` - Use Gunicorn server
- `--workers 4` - Run 4 worker processes
- `--threads 2` - 2 threads per worker
- `--timeout 120` - Wait 120 seconds max
- `--bind 0.0.0.0:$PORT` - Listen on all interfaces, port from environment
- `app:app` - Run the "app" variable from "app.py"

**Contributor:** Sanchit (deployment config)

---

**.env.example**

**Simple Explanation:**
Template for secrets file. Like a form you fill in with your passwords!

```bash
# Copy this file to .env and fill in YOUR values
SECRET_KEY=change-this-to-random-64-character-string
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password
DATABASE_URL=sqlite:///school_booking.db
```

**Contributor:** Sanchit (security config)

---

## PART 5: DOCUMENTATION FILES

**All in /Documentation folder:**

1. `1_Sanchit_Kaushal_Contribution.md` (30 pages)
2. `2_Chichebendu_Umeh_Contribution.md` (28 pages)
3. `3_Shiva_Kasula_Contribution.md` (35 pages)
4. `4_Mohd_Sharjeel_Contribution.md` (32 pages)
5. `5_Team_Collated_Documentation.md` (40 pages)
6. `6_Requirements_and_Installation.md` (25 pages)
7. `7_Code_Files_Explanation.md` (this file)

**Plus PDFs of all the above!**

---

## PART 6: PROJECT STATISTICS

**Code Metrics:**

```
Total Files: 52
├── Python: 8 files (3,200 lines)
├── HTML: 18 files (1,800 lines)
├── CSS: 2 files (600 lines)
├── JavaScript: 1 file (400 lines)
└── Documentation: 7 MD files (200+ pages)

Total Lines of Code: ~6,000
Comments: ~800 lines (13% documentation)
Blank Lines: ~600 lines
```

**File Size Distribution:**

```
Largest Files:
1. app.py - 1,300 lines (main application)
2. static/css/style.css - 500 lines (styling)
3. static/js/script.js - 400 lines (interactivity)
4. populate_db.py - 200 lines (test data)
5. config.py - 70 lines (configuration)
```

**Database Statistics:**

```
Tables: 8
Relationships: 12 foreign keys
Indexes: 15 (optimized queries)
Constraints: 8 (data integrity)
Sample Data: 100+ records
```

---

## PART 7: VIVA Q&A

**Q1: Explain the purpose of base.html and template inheritance.**

**Simple**: "base.html is like a house foundation - all pages build on top of it. Navigation and footer are in base.html so we don't repeat them 18 times!"

**Technical**: "Template inheritance using Jinja2's `{% extends %}` and `{% block %}` tags enables DRY principle. base.html defines common layout, child templates override specific blocks. Reduces code duplication from ~800 lines to ~200 lines across all templates."

---

**Q2: Why separate static files from templates?**

**Simple**: "Templates = HTML (structure), Static = CSS/JS/images (decoration). Like separating blueprint from paint/furniture. Makes organization clearer!"

**Technical**: "Separation of concerns - Flask serves static files via different route (/static/) with caching headers. Templates are processed server-side (Jinja2), static files served as-is. Enables CDN deployment and browser caching for performance."

---

**Q3: Explain the database initialization process.**

**Simple**: "populate_db.py creates empty database, then fills it with demo data. Like building a library (empty), then adding books (data)!"

**Technical**:
```python
db.drop_all()      # Delete existing tables
db.create_all()    # Create new tables from models
# Add sample data
db.session.add(admin)
db.session.add(parent)
db.session.commit()  # Save to database
```

Models define schema via SQLAlchemy ORM. `create_all()` generates SQL DDL statements. Transaction ensures atomic creation."

---

## Conclusion

The codebase demonstrates modular architecture with clear separation of concerns. Each component serves a specific purpose, from core application logic (app.py) to presentation (templates) to styling (CSS) to interactivity (JavaScript). Helper scripts automate deployment and testing. Comprehensive documentation ensures maintainability.

**Total Project Size:**
- 52 files
- 6,000+ lines of code
- 200+ pages of documentation
- 4 team members
- 7 weeks development

University of East London  
November 2025
