# School Activity Booking System

## 🏫 Project Overview
A comprehensive web-based application for managing school activity bookings, designed for **Greenwood International School**. This system streamlines the process of activity registration, payments, and attendance tracking for parents, tutors, and administrators.

**Developed for Module**: CN7021 - Advanced Software Engineering  
**Institution**: University of East London

---

## 👥 The Team

*Contributors to be added.*

---

## 🚀 Key Features

### 👨‍👩‍👧‍👦 For Parents
- **Secure Dashboard**: View children and active bookings.
- **Easy Booking**: Browse and book activities with real-time availability.
- **Waitlist System**: Automatically join waitlists for full classes.
- **Instant Confirmation**: Receive email confirmations with calendar invites (.ics).
- **Invoices**: Download professional PDF invoices.

### 👨‍🏫 For Tutors
- **🆕 Self-Registration**: Apply to become a tutor via public application form.
- **🆕 Application Tracking**: Receive email updates on application status.
- **Class Management**: View assigned activities and student lists (approved tutors only).
- **Attendance Tracking**: Mark student attendance digitally.
- **Real-time Updates**: See class capacity and enrollment.

### 🛡️ For Administrators
- **Control Panel**: Manage activities, tutors, and users.
- **🆕 Tutor Approval System**: Review and approve/reject tutor applications.
- **🆕 Email Notifications**: Automatic notifications for new applications.
- **Analytics**: View booking statistics and revenue.
- **Security**: RBAC (Role-Based Access Control) and CSRF protection.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask 2.3
- **Database**: SQLite (Dev), PostgreSQL (Prod), SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Security**: Scrypt Hashing, Flask-WTF (CSRF), Secure Sessions
- **Services**: Gmail SMTP (Emails), ReportLab (PDFs)

---

## 📚 Documentation

Detailed documentation is available in the `Documentation/` directory.

---

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/school-booking-system.git
   cd school-booking-system
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\Activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Update settings (Secret Key, Email credentials)

5. **Initialize Database**
   ```bash
   python populate_db.py
   ```

6. **Run Application**
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000`

---

## 📄 License
This project is for educational purposes only.
