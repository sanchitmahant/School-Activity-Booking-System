# School Activity Booking System - Setup Instructions

## 📋 System Requirements

### Prerequisites
- **Python**: 3.8 or higher (3.9+ recommended)
- **pip**: Python package installer (comes with Python)
- **Git**: For cloning the repository (optional)
- **Email Account**: Gmail account for sending emails (or configure SMTP)

### Operating Systems Supported
✅ Windows 10/11  
✅ macOS 10.14+  
✅ Linux (Ubuntu 20.04+, Debian, etc.)

---

## 🚀 Installation Steps

### Step 1: Download/Clone the Project

**Option A: Download ZIP**
1. Download the project as ZIP file
2. Extract to your desired location  
3. Open terminal/command prompt in the extracted folder

**Option B: Clone with Git**
```bash
git clone <repository-url>
cd School_Activity_Booking_System
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**If you encounter errors**, upgrade pip first:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root (optional, for production):

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_DEBUG=False

# Email Configuration (Gmail)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///school_system.db
```

**Note**: For Gmail, you need an "App Password" (not your regular password):
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Generate App Password for "Mail"
4. Use that 16-character password

### Step 5: Initialize the Database

The database will be created automatically on first run, but you can also initialize manually:

```bash
python
>>> from app import init_db
>>> init_db()
>>> exit()
```

### Step 6: Run the Application

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Step 7: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔐 Default Credentials

### Admin Account
- **Email**: `greenwoodinternationaluk@gmail.com`
- **Password**: `greenwood2024`

### Sample Tutor (Dr. Sarah Jenkins)
- **Email**: `drjenkins.greenwood@gmail.com`
- **Password**: `greenwood2024`

### Sample Parent
- **Email**: `sanchitmahant@gmail.com`
- **Password**: `greenwood2024`
- **Child**: Aryan Kaushal (Year 6)

---

## 📁 Project Structure

```
School_Activity_Booking_System/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── school_system.db        # SQLite database (auto-created)
├── templates/              # HTML templates
│   ├── admin/             # Admin portal templates
│   ├── tutor/             # Tutor portal templates  
│   ├── parent/            # Parent portal templates
│   └── *.html             # Shared templates
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
└── invoices/              # Generated PDFs (auto-created)
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Make sure virtual environment is activated and all dependencies installed:
```bash
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution**: Either:
1. Kill the process using port 5000
2. Change port in `app.py` (last line): `app.run(port=5001)`

### Issue: Emails not sending
**Solution**: 
1. Check Gmail App Password is correct in `.env`
2. Emails will print to console if email is not configured (development mode)
3. Check spam folder

### Issue: Database errors
**Solution**: Delete `school_system.db` and restart - it will rebuild automatically:
```bash
rm school_system.db    # Linux/macOS
del school_system.db   # Windows
python app.py
```

### Issue: "Template not found" error
**Solution**: Ensure you're running `python app.py` from the project root directory

---

## 🎯 Quick Start Guide

### For Development
1. Clone/download project
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python app.py`
5. Access: `http://127.0.0.1:5000`

### For Production
1. Set `FLASK_DEBUG=False` in `.env`
2. Change `SECRET_KEY` to a secure random string
3. Configure a production database (PostgreSQL recommended)
4. Use Gunicorn: `gunicorn app:app`
5. Set up reverse proxy (Nginx)
6. Use HTTPS

---

## 📚 Key Features

### Admin Portal
- Manage activities (create, edit, delete)
- Manage tutors (approve registrations, view profiles)
- View all bookings with filters
- Cancel bookings with email notifications
- Dashboard analytics

### Parent Portal
- Register and manage children
- Browse activities
- Make bookings
- View booking history
- Download invoices (PDF)
- Profile management

### Tutor Portal
- View assigned activities
- Track student attendance
- View earnings
- Profile management

---

## 🔄 Updating the Application

### Pull Latest Changes
```bash
git pull origin main
pip install -r requirements.txt  # Install any new dependencies
python app.py
```

### Backup Database
```bash
cp school_system.db school_system_backup_$(date +%Y%m%d).db
```

---

## 🆘 Support

For issues or questions:
1. Check this documentation first
2. Review error messages in terminal
3. Check browser console for front-end errors
4. Contact system administrator

---

## 📝 License & Credits

**School Activity Booking System**  
Developed for Greenwood International School  
© 2024 All Rights Reserved

---

## ✅ Post-Installation Checklist

After setup, verify:
- [ ] Server starts without errors
- [ ] Admin portal accessible and login works
- [ ] Parent portal accessible and login works
- [ ] Tutor portal accessible and login works
- [ ] Can create new activities
- [ ] Can register new tutors
- [ ] Can make bookings
- [ ] Emails send correctly (or print to console)
- [ ] PDFs generate for invoices

**If all checks pass, your installation is successful! 🎉**
