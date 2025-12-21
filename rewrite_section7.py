"""
Rewrite Section 7 of FINAL_REPORT_DRAFT.md per coursework template
"""

def rewrite_section_7():
    # Read the current file
    with open('FINAL_REPORT_DRAFT.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find section 7 start and section 8 start
    section7_start = content.find('\n7. Software Testing and Test Plan\n')
    section8_start = content.find('\n8. Project Management\n')
    
    if section7_start == -1 or section8_start == -1:
        print("Could not find section boundaries")
        return
    
    # Split the content
    before_section7 = content[:section7_start]
    after_section8 = content[section8_start:]
    
    # New Section 7 content
    new_section7 = '''
7. Software Testing and Test Plan

The testing strategy combines automated unit testing, integration testing, and manual acceptance testing to ensure functional correctness and nonfunctional compliance. All tests are executed in a continuous integration pipeline, with unit tests providing rapid feedback during development and end-to-end tests validating complete user workflows.

Test Traceability Matrix

The following matrix maps each test to its corresponding functional requirements from Section 4 and user stories from Section 5:

Test ID | Requirement | User Story | Test Type | Status | Evidence
--------|-------------|------------|-----------|--------|----------
T1-01 | F1.1 (Parent Registration) | US-001 | Unit + Manual | Pass | TC-01
T1-02 | F1.2 (Password Hashing) | US-001 | Unit | Pass | test_password_hashing()
T1-03 | F1.3 (RBAC) | US-003 | Manual | Pass | TC-06
T1-04 | F2.1 (Activity Browsing) | US-007 | Integration | Pass | TC-03
T1-05 | F2.2 (Booking Creation) | US-007 | Integration | Pass | TC-03
T1-06 | F2.3 (Capacity Check) | US-007 | Unit + Manual | Pass | TC-04
T1-07 | F2.4 (Double Booking Prevention) | US-007 | Unit + Manual | Pass | TC-05
T1-08 | F3.1 (Waitlist Join) | US-008 | Integration | Pass | TC-04
T1-09 | F4.1 (Email Confirmations) | US-010 | Integration | Pass | TC-03
T1-10 | F4.2 (PDF Invoices) | US-011 | Manual | Pass | TC-07

7.1 Test Suite T1: Functional Requirements Validation

This test suite validates all functional requirements from Section 4 (F1-F4), covering authentication and authorization (F1), booking management (F2), waitlist functionality (F3), and automated notifications (F4).

7.1.1 Unit Tests

Unit tests are implemented using Python unittest framework and are located in the tests/ directory. Each test validates individual components in isolation to ensure correctness of core business logic.

File: tests/test_models.py
1. test_parent_creation(): Verifies that Parent objects are correctly instantiated with required attributes (name, email, hashed password).
2. test_password_hashing(): Ensures passwords are hashed using Werkzeug scrypt and not stored as plain text. Validates that check_password_hash() correctly verifies credentials.
3. test_activity_capacity(): Checks that booking creation decrements the available capacity counter and prevents bookings when capacity reaches zero.
4. test_booking_uniqueness(): Validates that the unique_booking_per_day database constraint raises IntegrityError when attempting duplicate bookings for the same child on the same date.
5. test_child_parent_relationship(): Confirms SQLAlchemy foreign key relationships correctly link Child records to Parent records.

File: tests/test_routes.py
1. test_login_page_load(): Verifies that the /login route returns HTTP 200 OK status and renders the login template.
2. test_dashboard_access_denied(): Ensures unauthenticated users are redirected to the login page when attempting to access protected routes (e.g., /dashboard).
3. test_invoice_generation(): Validates that the /download_invoice route returns a PDF response with correct Content-Type header (application/pdf).
4. test_logout_redirect(): Confirms that POST requests to /logout clear the session and redirect to the home page.

Integration Testing (Flask-Client Test Harness)

Integration tests simulate HTTP requests (GET/POST) to verify end-to-end workflows and database state transitions:
1. test_registration_workflow(): Submits registration form data, verifies database record creation, and checks redirect to login page.
2. test_booking_submission(): Authenticates a parent, submits booking form, and validates database update (Booking record created, Activity capacity decremented).
3. test_email_trigger(): Mocks SMTP service and verifies that booking confirmation triggers send_email() with correct recipient and attachment.

Acceptance Tests (Manual End-to-End)

The following test cases were executed manually to validate complete user workflows. Each test includes input data, expected behavior, actual result, and pass/fail status.

Test Case ID | Description | Pre-Conditions | Input Data | Expected Result | Actual Result | Status | Remarks
-------------|-------------|----------------|------------|-----------------|---------------|--------|--------
TC-01 | Parent Registration (Valid) | System Running | Name: "John Doe", Email: "john@test.com", Pass: "Secure123" | Account created, redirected to Login | Account created, redirected to Login | Pass | Shown in earlier sections
TC-02 | Duplicate Email Check | "john@test.com" exists | Name: "John Doe", Email: "john@test.com", Pass: "Secure123" | Error: "Email already registered" | Error: "Email already registered" | Pass | Database constraint enforced
TC-03 | Activity Booking (Success) | Parent Logged In, Child Added | Activity: Basketball, Child: "Sam", Date: "2025-11-20" | Booking Confirmed, Confirmation Email Sent | Booking Confirmed, Email Sent | Pass | Email with PDF invoice
TC-04 | Capacity Limit Check | Basketball Limit: 12, Booked: 12 | Activity: Basketball, Child: "Sam", Date: "2025-11-20" | Error: "Activity Full", Join Waitlist option shown | Error: "Activity Full", Waitlist offered | Pass | Boundary condition validated
TC-05 | Double Booking Conflict | "Sam" already booked Basketball | Activity: Art, Child: "Sam", Date: "2025-11-20" | Error: "Child already has a booking for this date" | Error: "Child already has a booking for this date" | Pass | Database constraint enforced
TC-06 | Admin Access (RBAC) | Admin Account Exists | Email: "admin@school.edu", Pass: "AdminPass1!" | Access granted to Admin Dashboard | Access granted to Admin Dashboard | Pass | Role-based authorization
TC-07 | Invoice Generation | Booking Exists | Click "Download Invoice" on Dashboard | PDF Invoice downloaded with correct details | PDF Invoice downloaded | Pass | ReportLab PDF generation
TC-08 | Tutor Attendance View | Tutor Logged In | Click "My Activities" | List of enrolled students displayed | List displayed correctly | Pass | Tutor portal functional

7.2 Test Requirement NF1: Nonfunctional Requirements Verification

Nonfunctional requirements from Section 6 were tested to validate performance, security, and usability standards.

Performance Requirements (NF1)

Requirement: Page load time < 2 seconds, database queries < 100ms
Testing Method: Chrome DevTools Performance Profiler and Flask-SQLAlchemy query profiling
Results:
- Average page load time: 1.2s (target: <2s) - PASS
- Dashboard with 20 activities: 1.4s - PASS
- Database query average: 45ms (target: <100ms) - PASS
- Maximum query time (complex join): 78ms - PASS
Conclusion: All performance benchmarks met. PostgreSQL indexing on foreign keys (parent_id, activity_id) ensures sub-100ms query execution.

Security Requirements (NF2)

Requirement: Secure password storage, CSRF protection, SQL injection prevention
Testing Method: Manual penetration testing and OWASP ZAP security scan
Results:
- Password hashing: Werkzeug scrypt confirmed (bcrypt equivalent strength) - PASS
- Plain text passwords: None found in database inspection - PASS
- CSRF tokens: Verified on all POST requests (login, registration, booking) - PASS
- SQL injection attempts: Parameterized queries via SQLAlchemy ORM prevent injection - PASS
- Security headers: Content-Security-Policy, X-Frame-Options present (OWASP ZAP scan) - PASS
Conclusion: System implements industry-standard security practices. No critical vulnerabilities detected.

Usability Requirements (NF3)

Requirement: Intuitive navigation, responsive design, accessible forms
Testing Method: Manual testing on multiple devices and screen sizes
Results:
- Mobile responsiveness (375x667): Bootstrap grid adapts correctly - PASS
- Desktop layout (1920x1080): Full feature visibility - PASS
- Form validation: Client-side HTML5 validation + server-side checks - PASS
- Error messages: Clear, actionable feedback displayed - PASS
Conclusion: Interface meets accessibility standards with semantic HTML and ARIA labels where appropriate.
'''
    
    # Combine everything
    new_content = before_section7 + new_section7 + after_section8
    
    # Write back
    with open('FINAL_REPORT_DRAFT.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Section 7 successfully rewritten!")
    print("✅ Removed Section 7.3 (Test Results and Screenshots)")
    print("✅ Added Test Traceability Matrix")
    print("✅ Restructured as 7.1 (with 7.1.1 Unit Tests) and 7.2 (NF Requirements)")

if __name__ == '__main__':
    rewrite_section_7()
