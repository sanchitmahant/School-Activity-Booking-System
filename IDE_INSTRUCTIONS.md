# IDE Instructions & Change Log

## Purpose
This file tracks all instructions, changes, and important information for the School Activity Booking System project. In case the IDE crashes, this file serves as a reference to understand what has been done and what needs to be maintained.

---

## **🆕 MAJOR UPDATE: Professional Features Added (Dec 1, 2025)**

### Tutor Registration & Admin Approval System

**NEW FEATURE:** Tutors can now self-register through a public application form. Admins review and approve/reject applications.

**Key Changes:**
1. **Database Schema Updated:**
   - Added 5 new fields to Tutor model (status, application_date, approved_by, approval_date, email_verified)
   - Run `update_db_schema.py` to migrate existing databases

2. **New Routes:**
   - `/tutor/register` - Public tutor application form
   - `/admin/pending-tutors` - Admin review interface
   - `/admin/approve-tutor/<id>` - Approve application
   - `/admin/reject-tutor/<id>` - Reject application

3. **Email System:**
   - Automatic emails on application, approval, and rejection
   - Configured with Gmail SMTP in config.py

4. **Security:**
   - Tutors must be approved to login
   - Pending tutors see: "Your application is pending admin approval"
   - Rejected tutors cannot login

---

## Recent Changes & Fixes

### 2025-12-01: Professional Platform Enhancement
**Changes:**
- ✅ Tutor registration workflow with admin approval
- ✅ Email notification system (application, approval, rejection)
- ✅ Admin pending tutors management interface
- ✅ Database schema migration
- ✅ Enhanced UI templates

**Files Modified:**
- `app.py` - Added email functions and registration routes
- `templates/base.html` - Fixed tutor navigation
- `templates/tutor/register.html` - Created
- `templates/admin/pending_tutors.html` - Created

**Git Commit:** `b032a32`

### 2025-12-01: Tutor Navigation Fix
**Issue:** When tutors logged in, the navigation bar still showed "Login" instead of "Tutor Dashboard"

**Fix Applied:** Added tutor session check to `templates/base.html` (lines 46-49)

---

## Login Credentials (Development/Testing)

### Admin Account
- **Email:** greenwoodinternationaluk@gmail.com
- **Password:** sanchitkaushal

### Parent Test Account
- **Email:** parent@demo.com
- **Password:** demo123

### Tutor Accounts
All tutors use password: `tutor123`
- Dr. Sarah Jenkins: drjenkins.greenwood@gmail.com
- Prof. Michael Chen: michael.chen@greenwood.edu.uk
- Emma Thompson: emma.thompson@greenwood.edu.uk
- James Rodriguez: james.rodriguez@greenwood.edu.uk
- Dr. Amelia Watson: amelia.watson@greenwood.edu.uk
- David Park: david.park@greenwood.edu.uk

---

## Running the Application

### Start Development Server
```powershell
.venv\Scripts\activate
python app.py
```

Server runs at: http://127.0.0.1:5000

### Populate Database
```powershell
python populate_db.py
```

### Update Database Schema (for new tutor approval fields)
```powershell
python update_db_schema.py
```

---

## Git Workflow

### Always Keep GitHub Updated
After making any changes:
1. Check status: `git status`
2. Add changes: `git add .`
3. Commit with descriptive message: `git commit -m "Description of changes"`
4. Push to GitHub: `git push origin main`

---

## Email Configuration

### SMTP Settings
- **Server:** smtp.gmail.com:587
- **From Address:** greenwoodinternationaluk@gmail.com
- **Password:** Set in config.py (App Password required for Gmail)

### Email Templates
The system sends professional HTML emails for:
1. Tutor application confirmation
2. Admin new application notification
3. Tutor approval (with login instructions)
4. Tutor rejection (professional message)
5. Booking confirmations (already existed)

---

## Important Project Features

### Security Features
- CSRF protection on all forms
- Role-based access control (RBAC) with decorators
- Tutor approval workflow
- Custom 404 and 500 error pages
- Password hashing with Werkzeug

### Key Functionalities
1. **Parent Portal:**
   - Book activities for children
   - View and manage bookings
   - Download PDF invoices
   - Child profile management

2. **Admin Panel:**
   - Full CRUD for activities
   - User management
   - **🆕 Tutor application review**
   - Booking oversight
   - Reports and analytics

3. **Tutor Portal:**
   - **🆕 Self-registration via public form**
   - View assigned activities
   - Mark attendance
   - View attendance history

4. **Waitlist System:**
   - Automated waitlist management
   - Auto-enrollment when capacity available

---

## Database Schema
- SQLite database: `booking_system_v2.db`
- Models: Parent, Child, Activity, Booking, Admin, Tutor, Attendance, Waitlist
- **NEW:** Tutor model now includes approval workflow fields
- See `app.py` for model definitions

---

## File Structure
```
School_Activity_Booking_System/
├── app.py                          # Main Flask application (UPDATED)
├── config.py                       # Configuration with email settings
├── populate_db.py                  # Database population script
├── update_db_schema.py             # 🆕 Database migration script
├── templates/
│   ├── base.html                   # Base template (UPDATED)
│   ├── admin/
│   │   ├── dashboard.html
│   │   └── pending_tutors.html     # 🆕 Tutor approval interface
│   ├── tutor/
│   │   ├── register.html           # 🆕 Public registration form
│   │   ├── login.html
│   │   └── dashboard.html
│   └── parent/
├── static/
│   ├── css/
│   └── js/
└── Documentation/
```

---

## Testing Checklist
- [x] Parent login and booking flow
- [x] Admin CRUD operations
- [x] **🆕 Tutor registration flow**
- [x] **🆕 Admin approval/rejection**
- [x] **🆕 Email notifications**
- [x] Tutor attendance marking
- [x] PDF invoice generation with correct filenames
- [x] Waitlist functionality
- [x] CSRF protection
- [x] Custom error pages
- [x] Navigation bar for all user types

---

## Emergency Recovery Steps
1. Pull latest from GitHub: `git pull origin main`
2. Activate virtual environment: `.venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Check database schema: `python update_db_schema.py`
5. Start server: `python app.py`

---

## Notes for Future Development
- All changes are committed to GitHub (commit: b032a32)
- Test all three user portals (Parent, Admin, Tutor) after any changes
- Keep login credentials secure (use environment variables in production)
- Email system uses Gmail SMTP (set up App Password for production)
- Tutor approval workflow is production-ready

---

## Audio Transcription Process

For future reference, if you need to transcribe WhatsApp voice notes:

1. Install required packages:
   ```powershell
   .venv\Scripts\python.exe -m pip install SpeechRecognition pydub
   ```

2. Install ffmpeg:
   ```powershell
   winget install --id=Gyan.FFmpeg -e
   ```

3. Use the transcription scripts in the project root

---

**Last Updated:** December 1, 2025  
**Project Status:** Production-ready with professional tutor onboarding system  
**Latest Commit:** b032a32
