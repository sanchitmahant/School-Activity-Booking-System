# Individual Contribution Report: Shiva Kasula
**Role:** Full Stack Developer & Team Member

## Executive Summary
Shiva Kasula was responsible for 5 key components of the School Activity Booking System. Their contributions spanned across Waitlist System (Automated), Database Schema Design (3NF), ≡ƒåò Tutor Registration & Approval System, Calendar Integration (.ics Files), Role-Based Access Control (RBAC), demonstrating proficiency in full-stack development, database management, and system architecture.

## Detailed Contributions

### 1. Database Schema Design (3NF)
#### Simple Explanation (Non-Technical)
> In this task, I created normalized database with 7 models following third normal form.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
We designed a database schema strictly adhering to Third Normal Form (3NF) to eliminate redundancy and ensure data integrity. Our schema includes 7 interconnected models: Parent, Child, Activity, Booking, Tutor, Admin, and Waitlist. Each relationship is carefully mappedΓÇöfor example, we implemented a One-to-Many relationship from Parent to Child (one parent, many children) and from Activity to Booking. We avoid data duplication by using Foreign Keys; for instance, storing child_id in Booking rather than duplicating child data. This normalization ensures that updating a Child's name propagates automatically across all bookings, preventing database inconsistencies.

#### Code Logic & Implementation Details
**Key Files Involved:** `app.py, populate_db.py`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** What is Third Normal Form (3NF) and how did you apply it?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** Explain the relationship between the Parent and Child tables.
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How do you handle data integrity in your schema?
  - **A:** *[Prepare your answer based on the technical explanation above]*

---

### 2. Role-Based Access Control (RBAC)
#### Simple Explanation (Non-Technical)
> In this task, I implemented decorator-based rbac for three user types with separate portals.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
We implemented sophisticated Role-Based Access Control using Python decorators, demonstrating advanced software engineering. Three separate decorators enforce access: @login_required (for parents), @admin_required, and @tutor_required. Each decorator wraps route functions, checking session variables before execution and returning 403 Forbidden for unauthorized access. This is superior to inline checks because decorators are reusable, testable, and follow the DRY (Don't Repeat Yourself) principle. We created three distinct portal entry points (/login, /admin/login, /tutor/login), each with isolated dashboards, ensuring complete separation of concerns between user types.

#### Code Logic & Implementation Details
**Key Files Involved:** `app.py`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** How do your custom decorators enforce RBAC?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** Why is RBAC better than simple boolean flags for permissions?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** Can a user have multiple roles in your system?
  - **A:** *[Prepare your answer based on the technical explanation above]*

---

### 3. Waitlist System (Automated)
#### Simple Explanation (Non-Technical)
> In this task, I built intelligent automated waitlist with automatic promotion mechanism.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
We engineered an automated waitlist system demonstrating advanced algorithmic thinking. When activity capacity is reached, users are offered waitlist placement. Our algorithm: (1) Create Waitlist entry with timestamp and status='waiting'. (2) On booking cancellation, trigger check_waitlist_and_promote() function. (3) Query Waitlist table filtering by activity_id AND request_date AND status='waiting'. (4) Order results by created_at ascending (FIFO queue). (5) Select first entry using first(). (6) Atomically create new Booking, update Waitlist status to 'promoted', and commit transaction. This automatic promotion eliminates manual intervention and ensures fairness. We would enhance this with email notifications in production.

#### Code Logic & Implementation Details
**Key Files Involved:** `app.py`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** Explain the algorithm for automatic waitlist promotion.
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How do you ensure fairness in the waitlist queue?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** What triggers the promotion of a student from the waitlist?
  - **A:** *[Prepare your answer based on the technical explanation above]*

---

### 4. Calendar Integration (.ics Files)
#### Simple Explanation (Non-Technical)
> In this task, I implemented icalendar standard for automated calendar addition.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
We implemented the iCalendar (RFC 5545) standard to generate .ics files, demonstrating our ability to work with industry protocols. Our generate_ics_file() function: (1) Parses activity start_time and end_time strings. (2) Combines with booking_date to create datetime objects. (3) Formats as iCalendar DTSTART and DTEND (YYYYMMDDTHHmmss format). (4) Constructs .ics file content following RFC specification including VCALENDAR wrapper, VEVENT properties, VALARM for 24-hour reminders, and ORGANIZER field. (5) Attaches to email as text/calendar MIME type. When users receive the email, clicking the .ics file adds the activity to their calendar (Google Calendar, Outlook, Apple Calendar) with automatic remindersΓÇöa feature typically seen only in commercial booking systems.

#### Code Logic & Implementation Details
**Key Files Involved:** `app.py`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** What is the iCalendar standard (RFC 5545)?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How do you generate the unique content for the .ics file?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How does the user interact with the generated calendar file?
  - **A:** *[Prepare your answer based on the technical explanation above]*

---

### 5. ≡ƒåò Tutor Registration & Approval System
#### Simple Explanation (Non-Technical)
> In this task, I implemented professional tutor onboarding with application workflow and email notifications.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
We implemented a sophisticated tutor onboarding system transforming this project into a production-ready platform. This addresses the tutor feedback requirement for 'detailed tutor profile information that should be sent to admin for approval.' Implementation: (1) Database Schema Enhancement: Added 5 new fields to Tutor model (status: pending/approved/rejected, application_date, approved_by foreign key, approval_date, email_verified boolean). (2) Public Registration Form (/tutor/register): Professional application form accepting full_name, email, password, specialization, qualifications, bioΓÇöwith validation for email format, password strength (8+ chars), and duplicate checking. (3) Email Notification System: send_tutor_application_email() sends confirmation to applicant and notification to admin with application details and review link. (4) Admin Approval Interface (/admin/pending-tutors): Tabbed interface displaying Pending/Approved/Rejected tutors with one-click approve/reject buttons including approval/rejection email automation (send_tutor_approval_email(), send_tutor_rejection_email()). (5) Login Status Check: Updated tutor login to verify status='approved', showing pending message for unapproved tutors. (6) UI Enhancements: Added registration link to tutor login page. This workflow demonstrates industry-standard onboarding patterns and advanced email integration.

#### Code Logic & Implementation Details
**Key Files Involved:** `app.py, templates/tutor/register.html, templates/admin/pending_tutors.html`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** Walk me through the tutor approval workflow.
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How do you secure the admin approval endpoints?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** What changes did you make to the database to support this feature?
  - **A:** *[Prepare your answer based on the technical explanation above]*

---
