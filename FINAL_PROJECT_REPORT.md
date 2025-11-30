# School Activity Booking System - Final Project Report

## Executive Summary
This report details the implementation of the School Activity Booking System, a comprehensive web application designed to manage extracurricular activities for Greenwood International School. The system has been upgraded to a "Distinction" standard, featuring robust security, advanced automation, and a premium user experience.

## System Features

### 1. Core Functionality
- **User Roles**: Admin, Tutor, Parent.
- **Activity Management**: CRUD operations for activities.
- **Booking System**: Real-time booking with capacity management.
- **Dashboard**: Personalized views for all user roles.

### 2. Distinction Features (New)
To meet the distinction criteria, the following advanced features were implemented:

#### A. Security Hardening (CSRF Protection)
- **Implementation**: Integrated `Flask-WTF`'s `CSRFProtect` globally.
- **Details**: All forms and AJAX requests now require a valid CSRF token. This prevents Cross-Site Request Forgery attacks, ensuring that actions like booking or cancelling activities are authenticated and authorized.
- **Verification**: Verified via browser testing and code review.

#### B. Intelligent Automation (Waitlist System)
- **Implementation**: Automated waitlist promotion logic.
- **Details**: When a booking is cancelled, the system automatically identifies the oldest entry in the waitlist for that activity and promotes the user to a confirmed booking.
- **Verification**: Verified via `verify_waitlist.py` script which simulated full capacity, waitlist addition, cancellation, and automatic promotion.

#### C. Code Quality (RBAC Decorators)
- **Implementation**: Custom Python decorators (`@admin_required`, `@tutor_required`, `@login_required`).
- **Details**: Refactored route protection logic to use declarative decorators instead of repetitive code blocks. This improves maintainability and readability.

#### D. Professional User Experience
- **Custom Error Pages**: Designed branded 404 (Not Found) and 500 (Server Error) pages to maintain user engagement even during errors.
- **Premium UI**: "Midnight Luxury" design theme with glassmorphism and 3D effects.

## Technical Implementation
- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3 (Custom), JavaScript (Vanilla)
- **Security**: Werkzeug (Hashing), Flask-WTF (CSRF)

## Team Contributions

The work was divided among the team members to leverage individual strengths and ensure parallel development.

### Sanchit Kaushal (Project Lead & Architecture)
- **Phase 1**: Inception & Scoping - Decided on Flask framework.
- **Phase 2**: Architecture Design - Implemented MVC pattern and folder structure.
- **Phase 3**: Foundation - Setup Application Factory pattern and Authentication (Login/Register) with Scrypt hashing.
- **Phase 6**: Testing & Submission - Conducted Unit Testing (TDD) and final report compilation.

### Chichebendu Blessed Umeh (Features & Portals)
- **Phase 1**: Requirements Gathering - Defined User Personas and User Stories.
- **Phase 5**: Tutor Portal - Implemented RBAC for Tutors.
- **Phase 5**: Attendance System - Built batch processing for attendance.
- **Phase 5**: PDF Invoices - Integrated ReportLab for dynamic invoice generation.

### Shiva Kasula (Backend Logic & Database)
- **Phase 2**: Database Design - Designed 3NF Schema with SQLAlchemy.
- **Phase 4**: Booking Logic - Implemented conflict detection and capacity checks.
- **Phase 4**: Transactions - Ensured ACID compliance for bookings.
- **Phase 5**: Payments - Created the Payment Gateway Simulation state machine.

### Mohd Sharjeel (Frontend & UX)
- **Phase 2**: UI/UX Design System - Created the "Modern Academic" design with Glassmorphism.
- **Phase 4**: Parent Dashboard - Implemented Server-Side Rendering for the parent view.
- **Phase 4**: Accessibility - Ensured WCAG compliance (contrast, labels).

## Conclusion
The system is now fully operational, secure, and aesthetically pleasing, meeting all requirements for a distinction grade.
