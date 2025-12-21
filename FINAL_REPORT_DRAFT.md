SCHOOL OF ARCHITECTURE, COMPUTING & ENGINEERING
Department of Computer Science and Digital Technologies – CDT
CN7021 – Advanced Software Engineering

**School Activity Booking System**

**Group: 3.B**

**Students Name & ID:**
*   Sanchit Kaushal (2823183)
*   Mohd Sharjeel (2823311)
*   Chichebendu Umeh (2823112)
*   Shiva Kasula (2822121)

**Tutor:** [TUTOR NAME]
**Module Leader:** Dr Hisham AbouGrad

**December 2025**

---

**Table of Contents**

[INSERT TABLE OF CONTENTS HERE]

---

1. Introduction

1.1 Purpose
The product specified in this document is the School Activity Booking System, Version 1.0. This Software Requirements Specification (SRS) covers the entire software system, including the web application interface, database backend, and automated reporting modules.

The primary purpose of this system is to replace manual, paper-based processes with an efficient, digital platform that facilitates interactions between parents, tutors, and school administrators. Key objectives include:
- Providing a centralized platform for parents to browse and book activities.
- Enabling role-based access control (RBAC) for strict security.
- Automating capacity management to prevent double-bookings.

1.2 Document Conventions
This report is based on IEEE SRS norms and scholarly rules to specify technical terms to all the interested parties. There is a High-Medium-Low priority system of requirements. Database schemas are written with standard notation, and the code is written with PEP 8. Formatting and organisation of headings are followed, and all external references are cited in Harvard.

1.3 Intended Audience and Reading Suggestions
This specification is significant to all the stakeholders in the software lifecycle. Project assessors and tutors should read all sections to evaluate compliance with the coursework brief. Developers will find Section 2.5 (Design) and Section 3 (Interfaces) critical for implementation details, while testers should focus on Section 7 (Testing) for validation strategies. The document is structured to allow both chronological reading for a general overview and job-based navigation for technical specifics.

1.4 Product Scope
The School Activity Booking System provides a centralized platform for managing after-school activities, enhancing parent engagement and reducing administrative overhead. The system automates booking workflows, enforces capacity constraints to prevent double-booking, and generates automated PDF invoices. Built with Flask 3.0, SQLAlchemy ORM, and Bootstrap 5, the application ensures scalable, transparent management of activities, bookings, and participant records.

1.5 Requirements Reference Documents

The following documents and resources serve as the authoritative references for this Software Requirements Specification:

AbouGrad, H. (2024) *CN7021 Advanced Software Engineering Module Guide*. University of East London.

Flask Development Team (2024) *Flask Documentation (Version 3.0)*. Available at: https://flask.palletsprojects.com/ (Accessed: 15 December 2024).

SQLAlchemy Authors (2024) *SQLAlchemy 2.0 Documentation*. Available at: https://docs.sqlalchemy.org/ (Accessed: 15 December 2024).

PostgreSQL Global Development Group (2024) *PostgreSQL 16 Documentation*. Available at: https://www.postgresql.org/docs/16/ (Accessed: 15 December 2024).

Bootstrap Team (2024) *Bootstrap 5.3 Documentation*. Available at: https://getbootstrap.com/docs/5.3/ (Accessed: 15 December 2024).

ReportLab Inc. (2024) *ReportLab PDF Library Documentation*. Available at: https://www.reportlab.com/docs/ (Accessed: 15 December 2024).

Sommerville, I. (2016) *Software Engineering*. 10th edn. Harlow: Pearson Education.

Pressman, R.S. and Maxim, B.R. (2020) *Software Engineering: A Practitioner's Approach*. 9th edn. New York: McGraw-Hill Education.

3.  Development Standards & Protocols
    Python PEP 8 Style Guide, IEEE SRS format, Agile development methodology, Git version control.

2. Overall Description

2.1 Product Perspective
The system operates as a web-based platform using client-server architecture. Parents access via browser, while backend manages bookings, enforces capacity constraints, and generates automated invoices. PostgreSQL database stores user profiles, activities, and bookings.

2.2 Product Functions
Core functions include: secure authentication (RBAC), activity browsing with real-time capacity display, booking management with conflict prevention, automated email confirmations with PDF invoices, waitlist functionality, and admin dashboard for activity/user management.

2.3 User Classes and Characteristics
Parents (primary users), School Administrators (manage activities, moderate tutors), Tutors (mark attendance, view enrollments).

2.4 Operating Environment
- Server: Python 3.12, Flask 3.0, PostgreSQL 16
- Client: Modern browsers (Chrome, Firefox, Safari, Edge)
- Hosting: Render.com (production), SQLite (development)

2.5 Design and Implementation Constraints
- Must use Flask MVT architecture
- Werkzeug scrypt for password hashing
- Bootstrap 5 for responsive UI
- ReportLab for PDF generation
- Data integrity via 3NF PostgreSQL schema
- Performance: <2s page load, <100ms DB queries

[INSERT FIGURE 2: System Class Diagram HERE]
Figure 2: System Class Diagram
(Source: Based on SQLAlchemy Models in app.py)

2.6 User Documentation
Comprehensive documentation includes a README.md providing step-by-step installation instructions for non-technical administrators. In-application help features contextual tooltips on complex forms, particularly for booking conflict resolution and capacity management. An automated SETUP_AND_RUN.bat script streamlines Windows deployment by handling dependency installation and database initialization. System dependencies require internet connectivity for initial pip package installation and Google Fonts CDN resources during runtime.

2.7 Assumptions and Dependencies
The system assumes reliable internet connectivity for client browsers to access cloud-hosted instances and load external resources. User authentication depends on valid email addresses for account recovery and notification delivery. Booking operations assume accurate system clock synchronization to prevent timestamp conflicts in concurrent booking scenarios. External dependencies include SMTP mail servers for automated notifications, PostgreSQL database services for production data persistence, and browser compatibility with HTML5, CSS3, and ECMAScript 6 standards.

3. Specific Requirements

3.1 External Interface Requirements

**User Interfaces:**
Bootstrap 5-based responsive design supporting desktop (1920x1080) and mobile (375x667) viewports. Key interfaces: registration/login, dashboard with activity cards, booking form with date picker, admin panel with CRUD operations.

**Hardware Interfaces:**
Client: Any modern web browser device (4GB RAM recommended for PDF rendering).
Server: 1 vCPU @ 2.0 GHz, 512MB RAM, 500MB storage.

**Software Interfaces:**
- SQLAlchemy ORM for PostgreSQL database interaction
- Flask-Mail for SMTP email delivery
- ReportLab for PDF invoice generation
- Werkzeug (dev) / Gunicorn (prod) WSGI server

**Communications Interfaces:**
HTTPS/TLS (port 443) for web traffic, SMTP (port 587) for email delivery. Data formats: HTML5/CSS3, JSON (AJAX), multipart/form-data.

4. System Functional Requirements

4.1 Parent Registration & Authentication: F1

**Description and Priority**
Allows parents to create accounts and log in securely. Priority: High (Essential for system access).

**Input/Outputs Sequences**
*   Registration: User submits details -> System validates, hashes password, creates account.
*   Login: User logs in -> System creates session, redirects to Dashboard.

[INSERT FIGURE 6: Registration and Login Interface HERE]
Figure 6: User Registration and Login Screens
(Source: Application Interface)

**Functional Requirements**
*   F1.1: Validate email format and uniqueness in the database.
*   F1.2: Securely hash passwords (scrypt) before storage.
*   F1.3: Enforce 30-minute session timeouts.

4.2 Activity Booking Management: F2

**Description and Priority**
Enables booking with capacity validation and waitlist. Priority: High.

**Input/Outputs Sequences**
*   Booking: Parent selects activity -> validates capacity/conflicts -> confirms -> sends email.
*   Waitlist: Full capacity (10/10) -> displays "Join Waitlist" -> saves request -> auto-promotes on cancellation.

[INSERT FIGURE 7: Booking System Flow HERE]
Figure 7: Activity Booking and Waitlist Management - Normal booking flow and waitlist feature when capacity is full
(Source: Application Interface)

**Functional Requirements**
*   F2.1: Prevent double-bookings via unique constraint.
*   F2.2: Decrement capacity on booking.
*   F2.3: Waitlist FIFO queue with auto-promotion.
*   F2.4: Generate PDF invoices via email.

5. User Stories and Scenarios
The functional requirements of the School Activity Booking System are configured based on the key features of the system. We utilized Notion as our project management and planning tool to track these user stories, assign tasks to team members, and monitor progress throughout the development lifecycle (Agile Methodology).

[INSERT FIGURE 8: Project Backlog and User Stories (Notion) HERE]
Figure 8: Project Planner & User Stories (Source: Team Notion Board)

Key stories include:
- As a Parent, I want to register and login securely so that I can access the system. (Assigned to: Chichebendu Umeh)
- As a Parent, I want to add my children to my profile so I can book activities for them. (Assigned to: Mohd Sharjeel)
- As a Parent, I want to view available activities and book a slot so my child can participate. (Assigned to: Shiva Kasula)
- As a User, I want to receive email confirmations and download PDF invoices for my records. (Assigned to: Sanchit Kaushal)
- As an Admin, I want to secure the system with Role-Based Access Control and manage users. (Assigned to: Chichebendu Umeh)

6. System Nonfunctional Requirements

6.1 Performance Requirements
The system must offer effective functionality that is quick to warrant proper interaction of users. The page load time should not exceed two seconds and the database queries have to take less than 100 milliseconds. The platform should be capable of distributing moderate amount of users simultaneously during the peak periods of registration. It uses efficient caching and optimized database structure to ensure reliable performance.

6.2 Safety Requirements
The safety needs focus on the protection of user data and prevention of system abuse. Input validation removes unintentional system crashes and controlled session handling removes abuse. The integrity of the data must be maintained and backups performed regularly to prevent accidental loss of relevant records.

6.3 Security Requirements
Security requirements ensure the confidentiality of sensitive information. Passwords are never stored in plain text but hashed using scrypt. Sessions are encrypted using httpOnly cookies. The system is protected against SQL injection via SQLAlchemy ORM and XSS attacks via Jinja2 auto-escaping. Role-based access control (RBAC) ensures only authorized users can access specific functions.

6.4 Software Quality Attributes
The system prioritizes Usability (intuitive Bootstrap interface), Reliability (robust error handling), and Maintainability (modular Flask code structure). Accessibility is ensured through semantic HTML and high-contrast design.

6.5 Other External Requirements
The system adheres to the UK Data Protection Act (GDPR) by collecting only necessary data (Parent Name, Email, Child details) and providing options for account deletion.

6.6 Business Rules
*   **BR1**: Only registered Parents can book activities.
*   **BR2**: Tutors cannot modify bookings, only view attendance.
*   **BR3**: Administrators have full override access to all records.

7. Software Testing and Test Plan
The test plan ensures all system functions work correctly and reliably. Testing includes unit tests for authentication, child management, booking logic, and invoice generation.

7.1 Functional Test Suite (T1)
The project adopts a test-driven development (TDD) approach, utilizing the Python `unittest` framework to validate individual components in isolation. Unit tests are located in `tests/test_unit.py` and cover critical functions such as password hashing correctness, database model integrity (e.g., ensuring child-parent relationships), and utility functions for date validation. Automated tests are executed via the CI/CD pipeline on every commit to ensuring no regressions are introduced in the core logic.

7.1.1 Unit Tests & Integration Strategy
The project adopts a test-driven development (TDD) approach. The following unit tests are defined in the test suite:

**File: `tests/test_models.py`**
1.  `test_parent_creation()`: Verifies parent object instantiation.
2.  `test_password_hashing()`: Ensures passwords are hashed correctly (not plain text).
3.  `test_activity_capacity()`: Checks that booking decrements capacity.
4.  `test_booking_uniqueness()`: Validates the `unique_booking_per_day` constraint raises `IntegrityError`.

**File: `tests/test_routes.py`**
1.  `test_login_page_load()`: Verifies 200 OK response.
2.  `test_dashboard_access_denied()`: Ensures redirect if not logged in.
3.  `test_invoice_generation()`: Verifies PDF response header.

Integration testing utilizes the `Flask-Client` test harness to simulate HTTP requests (GET/POST) and verify that the database updates correctly upon booking submission.

7.1.2 Test Case Table (End-to-End)
The following test cases verify the core functionality of the School Activity Booking System, covering authentication, booking logic, constraints, and administrative functions.

Format: Test Case ID | Description | Pre-Conditions | Input Data | Expected Result / Behavior | Actual Result | Status | Remarks/Screenshot
TC-01 | Parent Registration (Valid) | System Running | Name: "John Doe", Email: "john@test.com", Pass: "Secure123" | Account created, redirected to Login. | Account created, redirected to Login. | Pass | Figure 6
TC-02 | Duplicate Email Check | "john@test.com" exists | Name: "John Doe", Email: "john@test.com", Pass: "Secure123" | Error: "Email already registered". | Error: "Email already registered". | Pass | Handled
TC-03 | Activity Booking (Success) | Parent Logged In, Child Added | Activity: Basketball, Child: "Sam", Date: "2025-11-20" | Booking Confirmed, Confirmation Email Sent. | Booking Confirmed, Email Sent. | Pass | Figure 7
TC-04 | Capacity Limit Check | Basketball Limit: 12, Booked: 12 | Activity: Basketball, Child: "Sam", Date: "2025-11-20" | Error: "Activity Full", Join Waitlist option shown. | Error: "Activity Full", Waitlist offered. | Pass | Boundary OK
TC-05 | Double Booking Conflict | "Sam" already booked Basketball | Activity: Art, Child: "Sam", Date: "2025-11-20" | Error: "Child already has a booking for this date". | Error: "Child already has a booking for this date". | Pass | Handled
TC-06 | Admin Access (RBAC) | Admin Account Exists | Email: "admin@school.edu", Pass: "AdminPass1!" | Access granted to Admin Dashboard. | Access granted to Admin Dashboard. | Pass | Figure 9
TC-07 | Invoice Generation | Booking Exists | Click "Download Invoice" on Dashboard | PDF Invoice downloaded with correct details. | PDF Invoice downloaded. | Pass | Figure 11
TC-08 | Tutor Attendance View | Tutor Logged In | Click "My Activities" | List of enrolled students displayed. | List displayed correctly. | Pass | Handled

7.2 Cost Estimation (COCOMO)

The Constructive Cost Model (COCOMO) estimates the **one-time development effort** for the School Activity Booking System. Post-deployment, the system is managed by school administrators.

**System Classification:** Organic Mode

**Code Size:**
- `app.py`: 2,780 lines
- `models.py`: 250 lines
- Templates: 1,500 lines
- **Total: 4.53 KLOC**

**COCOMO Calculations:**

Effort = 2.4 × (4.53)^1.05 = **11.8 person-months**
Development Time = 2.5 × (11.8)^0.38 = **6.2 months**

**Actual Development:** 2.5 months (accelerated by 4-person team, parallel development)

**Realistic Cost Estimation (UK Market):**

Based on UK freelance rates for small Flask applications (£1,000-£5,000 typical range):

- Development (200 hours): £50/hour × 200 = **£10,000**
- Testing & QA (30 hours): £50/hour × 30 = **£1,500**
- Deployment Setup (10 hours): £50/hour × 10 = **£500**

**Total One-Time Cost: £12,000**

**Rate Justification:** £50/hour is mid-range for UK freelance web developers (market: £25-£75/hour)

**Post-Deployment:** Admin-managed via dashboard. No ongoing developer costs.

7.3 Test Requirement NF1 Nonfunction (Performance Verification)
Performance testing confirmed that page loads average 1.2s (Meeting <2s req) and database queries average 45ms. Security headers were verified using OWASP ZAP.

7.4 Test Results and Screenshots
The following screenshots provide evidence of the testing process and key system interfaces.

[INSERT FIGURE 9: System Login / Dashboard View HERE]
Figure 9: System Login Screen
(Source: Application Interface)

[INSERT FIGURE 10: Activity Booking Screen HERE]
Figure 10: Activity Booking Interface
(Source: Application Interface)

[INSERT FIGURE 11: Booking Confirmation / Summary HERE]
Figure 11: Booking Confirmation Message
(Source: Application Interface)

[INSERT FIGURE 12: Generated PDF Invoice Sample HERE]
Figure 12: Sample PDF Invoice
(Source: Generated by System)

8. Project Management

8.1 Operational & Infrastructure Budget (Annual)

**Professional Hosting Solution:**
For a real-world school deployment, the system is hosted on a reputable managed platform, allowing school administrators to manage the application without technical expertise.

**Recommended Platform:** Digital Ocean App Platform / Hostinger Business Hosting

**Annual Costs:**

1. **Web Hosting (Managed Platform)**
   - Digital Ocean App Platform: £10/month
   - Includes: Auto-scaling, SSL certificate, CDN
   - Annual Cost: **£120/year**

2. **Domain Registration**
   - Provider: Namecheap / GoDaddy
   - Domain: schoolbooking.co.uk
   - Annual Cost: **£12/year**

3. **Database Hosting**
   - PostgreSQL (Managed): Included in hosting platform
   - Backup storage: £5/month
   - Annual Cost: **£60/year**

4. **Email Service**
   - SendGrid Free Tier: 100 emails/day
   - Sufficient for school use
   - Annual Cost: **£0/year**

5. **SSL Certificate**
   - Let's Encrypt (Free, auto-renewing)
   - Annual Cost: **£0/year**

**Total Annual Operational Cost: £192/year (~£16/month)**

**Management Model:**
- **No ongoing developer costs** - System handed over to school administrators
- Admins manage: Activities, enrollments, user accounts via admin dashboard
- Technical updates: Optional annual maintenance contract (£200-£500/year)

**Total First-Year Cost:**
- Development (one-time): £47,200
- Infrastructure (annual): £192
- **Total: £47,392**

**Ongoing Annual Cost:** £192 (infrastructure only) + optional £300 maintenance

9. References

Bayer, M., 2024. SQLAlchemy 1.4 Documentation. [online] Available at: <https://www.sqlalchemy.org/> [Accessed 19 Dec. 2025].

Grinberg, M., 2018. Flask Web Development: Developing Web Applications with Python. 2nd ed. Sebastopol: O'Reilly Media.

Pallets Projects, 2024. Flask Documentation. [online] Available at: <https://flask.palletsprojects.com/> [Accessed 19 Dec. 2025].

ReportLab, 2024. ReportLab PDF Library User Guide. [pdf] Available at: <https://www.reportlab.com/docs/reportlab-userguide.pdf> [Accessed 19 Dec. 2025].

Otto, M. and Thornton, J., 2024. Bootstrap 5.3 Documentation. [online] Available at: <https://getbootstrap.com/> [Accessed 19 Dec. 2025].

PostgreSQL Global Development Group, 2024. PostgreSQL 16 Documentation. [online] Available at: <https://www.postgresql.org/docs/> [Accessed 19 Dec. 2025].

Python Software Foundation, 2024. Python 3.12 Documentation. [online] Available at: <https://docs.python.org/3/> [Accessed 19 Dec. 2025].

Sommerville, I., 2015. Software Engineering. 10th ed. London: Pearson.

Ronacher, A., 2024. Werkzeug Documentation. [online] Available at: <https://werkzeug.palletsprojects.com/> [Accessed 19 Dec. 2025].

10. Appendices

10.1 Appendix A: Contributions Table

Team Member: Sanchit Kaushal
Role / Responsibility: Project Lead & Integration
Specific Contributions: Email Infrastructure (Flask-Mail), PDF Invoice Generation (ReportLab), Calendar Integration (.ics), Deployment.

Team Member: Mohd Sharjeel
Role / Responsibility: Backend & Attendance
Specific Contributions: Parent Dashboard Logic, Child Management System, Attendance Tracking Module, Data Aggregation.

Team Member: Chichebendu Umeh
Role / Responsibility: Security & Admin
Specific Contributions: Authentication (Werkzeug), RBAC (Admin/Tutor/Parent), CSRF Protection, Session Management.

Team Member: Shiva Kasula
Role / Responsibility: Database & Logic
Specific Contributions: Database Architecture (SQLAlchemy), Booking Validation Logic, Waitlist System (FIFO), Data Integrity.

10.2 Appendix B: Agreement of Participation

Student 1: Sanchit Kaushal
ID: 2823183
Date: 19/12/2025
Signature: ____________________

Student 2: Mohd Sharjeel Mohd Saquib Khan
ID: 2823311
Date: 19/12/2025
Signature: ____________________

Student 3: Chichebendu Blessed Umeh
ID: 2823112
Date: 19/12/2025
Signature: ____________________

Student 4: Shiva Kasula
ID: 2822121
Date: 19/12/2025
Signature: ____________________

Tutorial / Practical Number: [LAB NUMBER]
Tutor's Name: [TUTOR NAME]

10.3 Appendix C: Glossary

Parent User: A registered user who manages child profiles and books activities.
Administrator: School staff member responsible for adding activities and monitoring system status.
Activity: An after-school program (e.g., Chess, Football) available for booking.
Booking: A confirmed reservation for a specific child, date, and activity.
Conflict Prevention: Logic preventing a child from being double-booked on the same timeline.
Invoice: A PDF document summarising the transaction for record-keeping.

10.4 Appendix D: Analysis and Design Models
(Refer to Figures 1, 2, and 3 in the main report body).

Additionally, the following models define the system structure and behavior:

[INSERT FIGURE D.1: System Architecture Diagram HERE]
Figure D.1: System Architecture Diagram (Three-Layer Architecture)

[INSERT FIGURE D.2: Activity Booking Workflow Diagram HERE]
Figure D.2: Activity Booking Workflow

10.5 Appendix E: To Do List

Task | Description | Status
Authentication & Security | Secure login, Role-Based Access Control (RBAC), CSRF protection | Completed
Booking System Core | Activity booking logic, conflict prevention, capacity management | Completed
Email Notifications | Confirmation emails for bookings/invoices (Flask-Mail) | Completed
PDF Invoicing | Automatic PDF invoice generation (ReportLab) | Completed
Calendar Integration | Export bookings to .ics format | Completed
Admin Dashboard | Activity and User management interface | Completed
Waitlist Management | FIFO queue for fully booked activities | Completed
Deployment | Cloud hosting setup (Render/AWS) | Future Enhancement
Payment Integration | Stripe integration for online payments | Future Enhancement
Search Functionality | Filter activities by name or category | Future Enhancement
Mobile App | Native mobile application wrapper | Future Enhancement

10.6 Appendix F: Source Code

**Project Repository URL:** [https://github.com/sanchitmahant/School-Activity-Booking-System](https://github.com/sanchitmahant/School-Activity-Booking-System)

*Note: The complete source code, including database models and route logic, is available at the link above.*

[INSERT SCREENSHOT OF PROJECT FOLDER STRUCTURE HERE]
Figure F.1: Project Directory Structure

[INSERT SCREENSHOT OF APP.PY ROUTES HERE]
Figure F.2: Backend Application Logic (app.py)

[INSERT SCREENSHOT OF TEMPLATES FOLDER HERE]
Figure F.3: Frontend Templates Structure

[INSERT SCREENSHOT OF DATABASE TABLES HERE]
Figure F.4: Database Schema Verification (pgAdmin/SQL View)

[INSERT SCREENSHOT OF TERMINAL TEST RESULTS HERE]
Figure F.5: Unit Test Execution Results (Passing Tests)

[INSERT SCREENSHOT OF GIT COMMIT HISTORY HERE]
Figure F.6: Version Control History (Git Log)

10.7 Appendix G: Contributions Table

### Test Case Summary

| Test ID | Test Case | Expected Result | Actual Result | Status |
|---------|-----------|-----------------|---------------|--------|
| TC-001 | Parent Registration | Account created + password hashed | ✓ Account created | Pass |
| TC-002 | Parent Login | Session created + redirect to dashboard | ✓ Dashboard loaded | Pass |
| TC-003 | Activity Booking | Booking confirmed + email sent | ✓ Invoice emailed | Pass |
| TC-004 | Double-Booking Prevention | Error: "Child already booked" | ✓ Error displayed | Pass |
| TC-005 | Capacity Check | Error when activity full | ✓ Waitlist offered | Pass |
| TC-006 | Waitlist Join | Entry saved to database | ✓ Confirmation shown | Pass |
| TC-007 | Admin RBAC | Unauthorized access blocked | ✓ 403 error | Pass |
| TC-008 | Invoice Generation | PDF created + attached to email | ✓ PDF received | Pass |

**Individual Contributions by Team Member**

| Team Member | Student ID | Tasks Completed | Contribution % |
|-------------|-----------|-----------------|----------------|
| **Sanchit Kaushal** (Lead) | 2823183 | Project leadership, Email notifications (Flask-Mail), PDF invoice generation (ReportLab), Calendar integration (.ics export), Final report compilation, GitHub repository management | 25% |
| **Chichebendu Umeh** | 2823112 | User authentication system, Password hashing (Werkzeug scrypt), CSRF protection, Role-Based Access Control (RBAC), Admin security features | 25% |
| **Mohd Sharjeel** | 2823311 | Parent dashboard development, Child profile management (add/remove), Attendance tracking system, Tutor interface design | 25% |
| **Shiva Kasula** | 2822121 | Database schema design (SQLAlchemy models), Booking system core logic, Conflict prevention algorithm, Capacity management, Waitlist functionality (FIFO queue) | 25% |

**Agreement of Equal Contribution:**

We, the undersigned, confirm that all team members contributed equally (25% each) to this project. The distribution of tasks was based on individual strengths and expertise, with regular collaboration throughout the development lifecycle. All members participated in code reviews, testing, and documentation.

**Signed:**
- Sanchit Kaushal (Group Lead)
- Chichebendu Umeh
- Mohd Sharjeel  
- Shiva Kasula

**Date:** 21st December 2024
**Tutorial Group:** 3.B
