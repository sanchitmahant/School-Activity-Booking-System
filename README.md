# 🏫 School Activity Booking System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

**A comprehensive, web-based platform for managing school extracurricular activities, bookings, and attendance.**

*(Developed by Group 3.B for CN7021 Advanced Software Engineering)*

</div>

---

## 📖 Overview

The **School Activity Booking System** is a robust web application designed to streamline the management of after-school activities for **Greenwood International School**. It replaces legacy manual processes with a secure, automated digital solution that serves three distinct user groups: **Admins**, **Tutors**, and **Parents**.

The system handles complex scheduling, real-time capacity management, waitlist automation, and secure payment processing logic, ensuring a seamless experience for all stakeholders.

## ✨ Key Features

### 🔐 Security & Access Control
- **Role-Based Access Control (RBAC):** Distinct dashboards for Admins, Tutors, and Parents.
- **Secure Authentication:** `Werkzeug` hashing for passwords and `Flask-Login` for session management.
- **CSRF Protection:** Integrated via `Flask-WTF` to prevent cross-site request forgery.

### 📅 Booking & Management
- **Real-Time Booking Engine:** Prevents double bookings and enforces capacity limits.
- **Smart Waitlists:** FIFO (First-In-First-Out) queue system that automatically promotes students when spots open up.
- **Attendance Tracking:** Tutors can mark attendance (Present/Absent/Late) with exportable reports.

### 📧 Notifications & Reporting
- **Automated Emails:** Instant confirmation emails with **.ics calendar attachments** for parents and tutors.
- **PDF Invoicing:** Professional PDF invoices generated on-the-fly using `ReportLab` with embedded QR codes.
- **Interactive Dashboards:** Visual overview of schedules, children, and payments.

---

## ⚙️ Architecture & Tech Stack

The application is built using the **Model-View-Template (MVT)** architectural pattern, ensuring separation of concerns and scalability.

| Component | Technology | Description |
|---|---|---|
| **Backend** | Python (Flask) | Core logic, routing, and controller functions. |
| **Database** | SQLAlchemy (ORM) | Abstraction layer for relational data models (Parents, Children, Bookings). |
| **Frontend** | Jinja2 + Bootstrap 5 | Dynamic HTML rendering with responsive design. |
| **Mail Server** | Flask-Mail | SMTP integration for transactional emails. |
| **Reporting** | ReportLab | Programmatic generation of PDF documents. |

---

## 👥 Team & Contributions

This project was built through the collaborative effort of **Group 3.B**, with each member owning specific technical modules.

| Team Member | Role | Core Technical Features Implemented |
|---|---|---|
| **Sanchit Kaushal** | Full Stack Developer | • **Notification System:** Built SMTP email triggers with calendar integration.<br>• **PDF Reporting:** Developed `enhanced_invoice.py` for dynamic invoice generation.<br>• **Waitlist Automation:** Implemented logic to promote students automatically. |
| **Mohd Sharjeel** | Backend (Child/Attendance) | • **Parent Portal:** CRUD operations for child management and age validation.<br>• **Tutor Portal:** Dashboard for viewing assigned classes.<br>• **Attendance Logic:** Backend logic for tracking student presence. |
| **Chichebendu Umeh** | Security & Admin | • **Authentication:** Secure Login/Register flows with password hashing.<br>• **Security:** Implemented CSRF protection and `@admin_required` decorators.<br>• **Admin Dashboard:** Central control panel for user management. |
| **Shiva Kasula** | Database & Booking | • **Database Schema:** Designed efficient ERD relations (One-to-Many).<br>• **Booking Engine:** Core algorithm for conflict detection and capacity checks.<br>• **Waitlist Logic:** Database structures for queue management. |

---

## 🚀 How to Run

### Prerequisite
- Python 3.10 or higher installed.

### Fast Setup (Windows)
1. **Clone/Download** this repository.
2. Double-click **`SETUP_AND_RUN.bat`**.
   - This script automatically creates a virtual environment, installs dependencies, initializes the database, and starts the server.
3. Open your browser to: `http://127.0.0.1:5000`

### Manual Setup
```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize Database
python init_db.py

# 5. Run Application
python app.py
```

### 🔑 Login Credentials (Demo)
| Role | Email | Password |
|---|---|---|
| **Admin** | `admin@greenwood.edu` | `admin123` |
| **Tutor** | `tutor@greenwood.edu` | `tutor123` |
| **Parent** | *(Register a new account)* | *(Any)* |

---

## 📸 Screenshots

*(Placeholders for project screenshots)*

| **Admin Dashboard** | **Booking Interface** |
|:---:|:---:|
| <img src="static/screenshots/admin_dashboard.png" alt="Admin Dashboard" width="400"> | <img src="static/screenshots/booking_page.png" alt="Booking Page" width="400"> |

| **PDF Invoice** | **Email Notification** |
|:---:|:---:|
| <img src="static/screenshots/invoice_sample.png" alt="Invoice" width="400"> | <img src="static/screenshots/email_sample.png" alt="Email" width="400"> |

---

<div align="center">
  <p>© 2025 Greenwood International School Project. All Rights Reserved.</p>
</div>
