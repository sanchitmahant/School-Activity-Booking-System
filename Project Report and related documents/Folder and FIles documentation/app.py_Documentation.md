# Documentation: app.py

**File Name**: `app.py`  
**Location**: Root Directory  
**Type**: Main Application Entry Point (Python)  
**Lines of Code**: ~2000+  

## Overview
`app.py` is the core of the School Activity Booking System. It initializes the Flask application, configures extensions (Database, Mail, CSRF), defines the database models, and contains all the route logic for the application.

## Key Components

### 1. Configuration & Initialization
- **Flask App**: Initialized with `Flask(__name__)`.
- **Database**: Uses `Flask-SQLAlchemy` with SQLite (`school_activities.db`).
- **Security**: Includes `Flask-WTF` for CSRF protection.
- **Email**: Configured using `Flask-Mail` with Gmail SMTP.
- **Login Manager**: Manages user sessions for Parents, Tutors, and Admins.

### 2. Database Models
- **Parent**: Stores parent user data, related to Children and Bookings.
- **Child**: Profile for students, linked to Parent.
- **Tutor**: Staff accounts for managing activities.
- **Activity**: Classes/events offered (Swiming, Music, etc.).
- **Booking**: Junction object linking Child, Activity, and Parent.
- **Waitlist**: Queue system for full activities.
- **Attendance**: **(Updated)** Tracks student presence with an added `notes` field.

### 3. Blueprint / Route Areas
- **Authentication**: `/login`, `/register`, `/logout` routes for different roles.
- **Parent Portal**: Dashboard for viewing bookings, adding children, and making new bookings.
- **Tutor Portal**: Dashboard for managing assigned activities and marking attendance.
- **Admin Dashboard**: Comprehensive control panel for users, activities, and reports.
- **API Endpoints**: JSON endpoints for AJAX requests (e.g., getting bookings).

## Recent Updates
- **Attendance Notes**: Added logic to the `Attendance` model and `tutor_attendance` route to support persistent notes for each student's attendance record.
- **Email Branding**: Updated all email sending functions to use the new "Greenwood International" professional HTML template.

## Dependencies
- `flask`, `flask_sqlalchemy`, `flask_login`, `flask_mail`, `flask_wtf`
