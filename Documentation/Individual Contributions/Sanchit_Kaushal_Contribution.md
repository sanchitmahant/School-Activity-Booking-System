# Individual Contribution Report: Sanchit Kaushal
**Role:** Full Stack Developer & Team Member

## Executive Summary
Sanchit Kaushal was responsible for 6 key components of the School Activity Booking System. Their contributions spanned across Phase 1, PDF Invoice Generation, Parent Portal Development, Phase 6, Payment Flow Implementation, Security Architecture, demonstrating proficiency in full-stack development, database management, and system architecture.

## Detailed Contributions

### 1. Phase 1: Inception & Scoping
#### Simple Explanation (Non-Technical)
> In this task, I decided to build school activity booking system from scratch using python flask.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
We deliberately chose to build this application from scratch using the Python Flask micro-framework rather than using a heavyweight framework like Django or a CMS. This decision was driven by the need for granular control over the application architecture, allowing us to implement advanced software engineering patterns such as the Application Factory Pattern, MVC architecture, and custom Role-Based Access Control. Flask's lightweight nature enabled us to maintain a modular codebase where each component serves a specific purpose, demonstrating our understanding of the Separation of Concerns principle.

#### Code Logic & Implementation Details
**Key Files Involved:** `app.py, requirements.txt`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** Why did you choose Flask over Django for this project?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** Explain the Application Factory Pattern and why it's useful.
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How does the MVC architecture apply to your Flask application?
  - **A:** *[Prepare your answer based on the technical explanation above]*

---

### 2. Security Architecture
#### Simple Explanation (Non-Technical)
> In this task, I implemented comprehensive security layer with csrf protection and password hashing.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
Security was our primary concern from inception. We implemented multiple security layers: (1) Password Security using Werkzeug's generate_password_hash which employs the Scrypt algorithm, a memory-hard key derivation function resistant to GPU-based brute-force attacks. (2) CSRF Protection via Flask-WTF, generating unique tokens for each form submission to prevent Cross-Site Request Forgery attacks. (3) Session Security using Flask's cryptographically signed cookies that prevent tampering. (4) Authorization Decorators that enforce Role-Based Access Control, ensuring parents cannot access admin routes and vice versa. (5) SQL Injection Prevention through SQLAlchemy's parameterized queries.

#### Code Logic & Implementation Details
**Key Files Involved:** `app.py, config.py`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** How does CSRF protection work in your application?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** Why did you use Scrypt for password hashing?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How do you prevent SQL injection attacks?
  - **A:** *[Prepare your answer based on the technical explanation above]*

---

### 3. Parent Portal Development
#### Simple Explanation (Non-Technical)
> In this task, I created comprehensive parent dashboard with booking management.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
The Parent Portal is the primary user interface, implementing Server-Side Rendering (SSR) with Jinja2 templates for optimal performance and SEO. Key features: (1) Dynamic Dashboard displaying children and their bookings using database joins to minimize queries. (2) AJAX-powered 'Add Child' modal providing seamless UX without page reloads. (3) Activity Browsing with real-time availability indicatorsΓÇöwe calculate available spots by subtracting confirmed bookings from max capacity, displayed with color-coded badges (green: available, orange: filling, red: full). (4) Progress Bars showing enrollment percentage with responsive color changes. (5) Booking Sidebar listing all confirmed bookings with status indicators.

#### Code Logic & Implementation Details
**Key Files Involved:** `app.py, templates/dashboard.html`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** How do you calculate real-time activity availability?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** Explain the AJAX implementation for adding a child.
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How does the dashboard handle database queries efficiently?
  - **A:** *[Prepare your answer based on the technical explanation above]*

---

### 4. Payment Flow Implementation
#### Simple Explanation (Non-Technical)
> In this task, I developed secure payment simulation with state machine approach.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
We implemented a realistic Payment Simulation using the State Machine pattern, mimicking real-world e-commerce systems. Flow: (1) User selects activity and date ΓåÆ State: 'Selection'. (2) System validates and redirects to payment page ΓåÆ State: 'Pending Payment'. (3) Payment form captures card details (simulated) with client-side validation. (4) On submission, system creates Booking with status='confirmed' and cost=activity.price ΓåÆ State: 'Confirmed'. (5) Redirect to confirmation page. This mimics the Two-Phase Commit protocol used by Stripe/PayPal where monetary transaction and order confirmation are separate operations. In production, we would integrate with a payment gateway API and implement webhook handlers for asynchronous payment confirmation.

#### Code Logic & Implementation Details
**Key Files Involved:** `app.py, templates/payment.html`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** Explain the state machine pattern used in your payment flow.
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How would you integrate a real payment gateway like Stripe?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** Why do you separate the payment confirmation from the booking creation?
  - **A:** *[Prepare your answer based on the technical explanation above]*

---

### 5. PDF Invoice Generation
#### Simple Explanation (Non-Technical)
> In this task, I developed professional pdf invoicing using reportlab library.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
We implemented programmatic PDF generation using the ReportLab library, going far beyond simple HTML-to-PDF conversion. Our generate_invoice() function: (1) Creates BytesIO buffer for in-memory PDF construction. (2) Initializes SimpleDocTemplate with A4 pagesize and margins. (3) Defines custom ParagraphStyles for typography hierarchy. (4) Constructs document using Platypus (Page Layout and Typography Using Scripts) framework. (5) Builds multi-section layout with Tables for structured data. Key sections: School Header with branding, Invoice Metadata (number, date, status), Client Information table, Activity Details, Itemized Charges with VAT breakdown, Payment Summary, Terms & Conditions. (6) Applies TableStyle for professional formatting with borders, backgrounds, and alignment. (7) Returns PDF via make_response with proper Content-Type and Content-Disposition headers forcing download.

#### Code Logic & Implementation Details
**Key Files Involved:** `enhanced_invoice.py, app.py`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** Why did you use ReportLab instead of HTML-to-PDF conversion?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** Explain how you draw tables and styles programmatically.
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How do you ensure the PDF is downloadable rather than just displayed?
  - **A:** *[Prepare your answer based on the technical explanation above]*

---

### 6. Phase 6: Deployment Preparation
#### Simple Explanation (Non-Technical)
> In this task, I prepared application for production deployment with configuration files.. This feature allows users to easily interact with the system by providing a seamless experience. It solves the problem of manual management by automating the process.

#### Technical Explanation (Detailed)
We prepared comprehensive deployment infrastructure demonstrating DevOps understanding: (1) requirements.txt listing all dependencies with specific versions for reproducibility. (2) Procfile defining web process as 'gunicorn app:app' for WSGI server deployment. (3) runtime.txt specifying Python 3.11.0 for platform consistency. (4) .env.example documenting required environment variables (SECRET_KEY, MAIL_USERNAME, MAIL_PASSWORD, DATABASE_URL). (5) .gitignore preventing sensitive data commits. (6) Updated config.py to read from environment variables enabling 12-Factor App compliance. (7) Prepared for SQLiteΓåÆPostgreSQL migration by ensuring SQLAlchemy queries are database-agnostic. (8) Created comprehensive README.md with installation instructions, features list, and usage guide.

#### Code Logic & Implementation Details
**Key Files Involved:** `requirements.txt, config.py, README.md`

**Implementation Strategy:**
1. Defined data models in `app.py` using SQLAlchemy.
2. Created route handlers (controllers) to process requests.
3. Implemented frontend templates using Jinja2 and Bootstrap.
4. Integrated validation logic to ensure data integrity.

#### Potential Viva Questions
- **Q:** What is the purpose of the Procfile?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** How do you manage environment variables in production?
  - **A:** *[Prepare your answer based on the technical explanation above]*
- **Q:** Explain the difference between the development and production configurations.
  - **A:** *[Prepare your answer based on the technical explanation above]*

---
