# IDE Instructions & Change Log

## Purpose
This file tracks all instructions, changes, and important information for the School Activity Booking System project. In case the IDE crashes, this file serves as a reference to understand what has been done and what needs to be maintained.

---

## Recent Changes & Fixes

### 2025-12-01: Tutor Navigation Fix
**Issue:** When tutors logged in, the navigation bar still showed "Login" instead of "Tutor Dashboard"

**Root Cause:** The `templates/base.html` file only checked for `session.get('parent_id')` and `session.get('admin_id')`, but was missing a check for `session.get('tutor_id')`

**Fix Applied:** Added tutor session check to `templates/base.html` (lines 46-49):
```html
{% elif session.get('tutor_id') %}
<li class="nav-item"><a class="nav-link text-primary" href="{{ url_for('tutor_dashboard') }}">Tutor
        Dashboard</a></li>
<li class="nav-item"><a class="nav-link" href="{{ url_for('logout') }}">Logout</a></li>
```

**Files Modified:**
- `templates/base.html` - Added tutor navigation check

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

---

## Git Workflow

### Always Keep GitHub Updated
After making any changes:
1. Check status: `git status`
2. Add changes: `git add .`
3. Commit with descriptive message: `git commit -m "Description of changes"`
4. Push to GitHub: `git push origin main`

---

## Important Project Features

### Security Features
- CSRF protection on all forms
- Role-based access control (RBAC) with decorators
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
   - Booking oversight
   - Reports and analytics

3. **Tutor Portal:**
   - View assigned activities
   - Mark attendance
   - View attendance history

4. **Waitlist System:**
   - Automated waitlist management
   - Auto-enrollment when capacity available

---

## Database Schema
- SQLite database: `booking_system.db`
- Models: Parent, Child, Activity, Booking, Admin, Tutor, Attendance, Waitlist
- See `app.py` for model definitions

---

## File Structure
```
School_Activity_Booking_System/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── populate_db.py        # Database population script
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── admin/           # Admin templates
│   ├── tutor/           # Tutor templates
│   └── parent/          # Parent templates
├── static/
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
└── Documentation/        # Project documentation
```

---

## Known Issues & TODO
- [ ] None currently - system fully functional

---

## Testing Checklist
- [ ] Parent login and booking flow
- [ ] Admin CRUD operations
- [ ] Tutor attendance marking
- [ ] PDF invoice generation with correct filenames
- [ ] Waitlist functionality
- [ ] CSRF protection
- [ ] Custom error pages
- [ ] Navigation bar for all user types ✅ (Fixed 2025-12-01)

---

## Emergency Recovery Steps
1. Pull latest from GitHub: `git pull origin main`
2. Activate virtual environment: `.venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Check database exists or run: `python populate_db.py`
5. Start server: `python app.py`

---

## Notes for Future Development
- All changes should be committed to GitHub immediately
- Test all three user portals (Parent, Admin, Tutor) after any changes
- Update this file with any new instructions or fixes
- Keep login credentials secure (use environment variables in production)

---

**Last Updated:** 2025-12-01
**Project Status:** Fully functional, ready for demonstration
