# School Activity Booking System

## 🏫 Project Overview
A comprehensive web-based application for managing school activity bookings, designed for **Greenwood International School**. This system streamlines the process of activity registration, payments, and attendance tracking for parents, tutors, and administrators.

**Developed for Module**: CN7021 - Advanced Software Engineering  
**Institution**: University of East London

---

## 👥 The Team

| Member | Role | Key Contributions |
|--------|------|-------------------|
| **Sanchit Kaushal** | Team Lead & Backend Security | Architecture, Auth System, Admin Portal, Security |
| **Chichebendu Blessed Umeh** | Integration Specialist | Email Notifications, PDF Generation, Tutor Portal |
| **Shiva Kasula** | Database Specialist | Database Design, Booking Logic, Waitlist System |
| **Mohd Sharjeel** | UI/UX Designer | Frontend Design, Responsive Layout, Accessibility |

---

## 🚀 Key Features

### 👨‍👩‍👧‍👦 For Parents
- **Secure Dashboard**: View children and active bookings.
- **Easy Booking**: Browse and book activities with real-time availability.
- **Waitlist System**: Automatically join waitlists for full classes.
- **Instant Confirmation**: Receive email confirmations with calendar invites (.ics).
- **Invoices**: Download professional PDF invoices.

### 👨‍🏫 For Tutors
- **Class Management**: View assigned activities and student lists.
- **Attendance Tracking**: Mark student attendance digitally.
- **Real-time Updates**: See class capacity and enrollment.

### 🛡️ For Administrators
- **Control Panel**: Manage activities, tutors, and users.
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

Detailed documentation is available in the `Documentation/` directory:

1. **[Security & Architecture (Sanchit)](Documentation/1_Sanchit_Kaushal_Contribution.md)**
2. **[Email & Integration (Chichebendu)](Documentation/2_Chichebendu_Umeh_Contribution.md)**
3. **[Database & Logic (Shiva)](Documentation/3_Shiva_Kasula_Contribution.md)**
4. **[UI/UX Design (Sharjeel)](Documentation/4_Mohd_Sharjeel_Contribution.md)**
5. **[Installation Guide](Documentation/6_Requirements_and_Installation.md)**

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
