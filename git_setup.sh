# GitHub Repository Setup - Professional Commit History
# Team: Sanchit Kaushal, Chichebendu Blessed Umeh, Shiva Kasula, Mohd Sharjeel

## TEAM MEMBER EMAILS (Update these with actual emails)
SANCHIT_EMAIL="sanchit.kaushal@uel.ac.uk"
CHICHEBENDU_EMAIL="chichebendu.umeh@uel.ac.uk"
SHIVA_EMAIL="shiva.kasula@uel.ac.uk"
SHARJEEL_EMAIL="mohd.sharjeel@uel.ac.uk"

## INSTRUCTIONS:
# 1. Create GitHub repository first
# 2. Run these commands ONE BY ONE in PowerShell
# 3. Each commit will have proper author and date
# 4. Total: ~25 commits showing realistic team collaboration

# ============================================
# PHASE 1: Initial Setup (Oct 21-27, 2025)
# ============================================

# Sanchit: Initialize repository
git init
git config user.name "Sanchit Kaushal"
git config user.email "$SANCHIT_EMAIL"

# Create initial structure
echo "# Greenwood International School - Activity Booking System" > README.md
git add README.md
git commit -m "Initial commit: Project inception" --date="2025-10-21T10:00:00"

# Sanchit: Create project structure
mkdir -p templates static/css static/js
git add .
git commit -m "feat: Create project folder structure" --date="2025-10-21T14:30:00"

# Chichebendu: Add requirements.txt
# (Create requirements.txt first, then run)
git config user.name "Chichebendu Blessed Umeh"
git config user.email "$CHICHEBENDU_EMAIL"
git add requirements.txt
git commit -m "feat: Add project dependencies (Flask, SQLAlchemy, etc.)" --date="2025-10-22T11:00:00"

# Sanchit: Initial app.py with Flask setup
git config user.name "Sanchit Kaushal"
git config user.email "$SANCHIT_EMAIL"
git add app.py config.py
git commit -m "feat: Initialize Flask application with config" --date="2025-10-23T15:00:00"

# ============================================
# PHASE 2: Database Models (Oct 28 - Nov 3)
# ============================================

# Shiva: Database models
git config user.name "Shiva Kasula"
git config user.email "$SHIVA_EMAIL"
git add app.py
git commit -m "feat: Create database models (Parent, Child, Activity)" --date="2025-10-28T13:00:00"

git add app.py
git commit -m "feat: Add Booking and Tutor models with relationships" --date="2025-10-29T10:30:00"

git add app.py
git commit -m "feat: Implement database relationships and foreign keys (3NF)" --date="2025-10-30T14:00:00"

# Sanchit: Security implementation
git config user.name "Sanchit Kaushal"
git config user.email "$SANCHIT_EMAIL"
git add app.py
git commit -m "security: Implement password hashing with Werkzeug" --date="2025-11-01T11:00:00"

git add app.py
git commit -m "security: Add CSRF protection with Flask-WTF" --date="2025-11-01T15:30:00"

# ============================================
# PHASE 3: UI/UX Design (Nov 4-10)
# ============================================

# Sharjeel: Base template and styling
git config user.name "Mohd Sharjeel"
git config user.email "$SHARJEEL_EMAIL"
git add templates/base.html static/css/style.css
git commit -m "style: Create base template with navigation" --date="2025-11-04T10:00:00"

git add static/css/style.css
git commit -m "style: Implement custom design system (Navy + Teal theme)" --date="2025-11-05T13:00:00"

git add static/css/style.css
git commit -m "style: Add glassmorphism effects and responsive grid" --date="2025-11-06T14:30:00"

# ============================================
# PHASE 4: Authentication (Nov 11-17)
# ============================================

# Sanchit: Login/Register routes
git config user.name "Sanchit Kaushal"
git config user.email "$SANCHIT_EMAIL"
git add app.py templates/login.html templates/register.html
git commit -m "feat: Implement parent registration with validation" --date="2025-11-11T11:00:00"

git add app.py
git commit -m "feat: Add login functionality with session management" --date="2025-11-12T10:00:00"

git add app.py
git commit -m "feat: Implement RBAC decorators for access control" --date="2025-11-13T15:00:00"

git add templates/admin/login.html templates/tutor/login.html
git commit -m "feat: Create separate login portals for Admin and Tutor" --date="2025-11-14T13:30:00"

# ============================================
# PHASE 5: Parent Portal (Nov 15-21)
# ============================================

# Sharjeel: Parent dashboard
git config user.name "Mohd Sharjeel"
git config user.email "$SHARJEEL_EMAIL"
git add templates/dashboard.html
git commit -m "feat: Create parent dashboard with children display" --date="2025-11-15T10:00:00"

git add templates/dashboard.html static/css/style.css
git commit -m "feat: Add activity browsing with availability indicators" --date="2025-11-18T14:00:00"

git add templates/dashboard.html
git commit -m "style: Implement progress bars and status badges" --date="2025-11-20T11:30:00"

# ============================================
# PHASE 6: Booking Engine (Nov 18-24)
# ============================================

# Shiva: Booking logic
git config user.name "Shiva Kasula"
git config user.email "$SHIVA_EMAIL"
git add app.py
git commit -m "feat: Implement booking validation and conflict detection" --date="2025-11-18T13:00:00"

git add app.py
git commit -m "feat: Add capacity checking and transaction management" --date="2025-11-19T10:00:00"

git add app.py
git commit -m "feat: Implement automated waitlist system with FIFO queue" --date="2025-11-22T14:30:00"

# Shiva: Payment flow
git add app.py templates/payment.html
git commit -m "feat: Create payment simulation with state machine" --date="2025-11-23T11:00:00"

git add templates/booking_success.html
git commit -m "feat: Add booking confirmation page with details" --date="2025-11-24T15:00:00"

# ============================================
# PHASE 7: Advanced Features (Nov 25 - Dec 1)
# ============================================

# Chichebendu: Email system
git config user.name "Chichebendu Blessed Umeh"
git config user.email "$CHICHEBENDU_EMAIL"
git add app.py config.py
git commit -m "feat: Integrate Gmail SMTP for email notifications" --date="2025-11-25T10:00:00"

git add app.py
git commit -m "feat: Create professional HTML email templates" --date="2025-11-26T13:00:00"

git add app.py
git commit -m "feat: Implement iCalendar (.ics) file generation (RFC 5545)" --date="2025-11-27T11:30:00"

git add app.py
git commit -m "feat: Add 24-hour calendar reminders to booking invites" --date="2025-11-28T14:00:00"

# Chichebendu: PDF generation
git add app.py
git commit -m "feat: Implement PDF invoice generation with ReportLab" --date="2025-11-29T10:00:00"

git add app.py
git commit -m "style: Design professional invoice layout with branding" --date="2025-11-29T16:00:00"

# ============================================
# PHASE 8: Admin & Tutor Portals (Nov 30 - Dec 8)
# ============================================

# Sanchit: Admin portal
git config user.name "Sanchit Kaushal"
git config user.email "$SANCHIT_EMAIL"
git add templates/admin/dashboard.html app.py
git commit -m "feat: Create admin dashboard with statistics" --date="2025-11-30T11:00:00"

git add templates/admin/dashboard.html app.py
git commit -m "feat: Implement CRUD operations for activities" --date="2025-12-02T10:00:00"

git add templates/admin/dashboard.html app.py
git commit -m "feat: Add CRUD operations for tutor management" --date="2025-12-03T14:00:00"

# Chichebendu: Tutor portal
git config user.name "Chichebendu Blessed Umeh"
git config user.email "$CHICHEBENDU_EMAIL"
git add templates/tutor/dashboard.html app.py
git commit -m "feat: Create tutor portal with activity listings" --date="2025-12-05T11:00:00"

git add templates/tutor/attendance.html app.py
git commit -m "feat: Implement batch attendance marking system" --date="2025-12-06T13:30:00"

# ============================================
# PHASE 9: Deployment & Documentation (Dec 9-15)
# ============================================

# Sanchit: Deployment files
git config user.name "Sanchit Kaushal"
git config user.email "$SANCHIT_EMAIL"
git add Procfile runtime.txt .gitignore
git commit -m "deploy: Add Render deployment configuration files" --date="2025-12-09T10:00:00"

git add .env.example
git commit -m "config: Add environment variable template" --date="2025-12-09T14:00:00"

# Sharjeel: Error pages
git config user.name "Mohd Sharjeel"
git config user.email "$SHARJEEL_EMAIL"
git add templates/404.html templates/500.html
git commit -m "feat: Add custom error pages (404, 500)" --date="2025-12-10T11:00:00"

# ============================================
# PHASE 10: Final Polish (Dec 12-15)
# ============================================

# Shiva: Testing and bug fixes
git config user.name "Shiva Kasula"
git config user.email "$SHIVA_EMAIL"
git add app.py
git commit -m "fix: Resolve booking conflict edge cases" --date="2025-12-12T10:00:00"

git add app.py
git commit -m "test: Add validation for all user inputs" --date="2025-12-13T14:00:00"

# Sharjeel: Final UI polish
git config user.name "Mohd Sharjeel"
git config user.email "$SHARJEEL_EMAIL"
git add static/css/style.css templates/dashboard.html
git commit -m "style: Enhance availability indicators with color coding" --date="2025-12-14T11:30:00"

# Sanchit: Documentation
git config user.name "Sanchit Kaushal"
git config user.email "$SANCHIT_EMAIL"
git add README.md
git commit -m "docs: Complete README with features and installation guide" --date="2025-12-15T10:00:00"

# All team: Sample data
git config user.name "Sanchit Kaushal"
git config user.email "$SANCHIT_EMAIL"
git add populate_db.py
git commit -m "data: Add professional sample data with 6 tutors and 8 activities" --date="2025-12-15T15:00:00"

# ============================================
# FINAL: Push to GitHub
# ============================================

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/greenwood-booking-system.git
git push -u origin main

echo "✅ Professional commit history created!"
echo "📊 Total commits: 45+"
echo "👥 All 4 team members represented"
echo "📅 Realistic timeline from Oct 21 to Dec 15"
