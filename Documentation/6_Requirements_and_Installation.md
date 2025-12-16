# Requirements & Installation Guide
**Project**: School Activity Booking System

---

## Simple Guide: How to Run This App

**Think of this like assembling furniture**:
You need the right tools, the parts, and the instructions.

---

## Part 1: The Tools You Need (Requirements)

Before you start, make sure your computer has these:

1. **Python** (The Engine)
   - This is the language our app speaks.
   - You need version 3.9 or newer.
   - Download from python.org

2. **Git** (The Downloader)
   - Helps you download our code.
   - Download from git-scm.com

3. **A Browser** (The Screen)
   - Chrome, Firefox, Edge, or Safari.
   - Any modern browser works!

---

## Part 2: Installation (Putting it Together)

Follow these steps exactly:

### Step 1: Get the Code
Open your terminal (Command Prompt) and type:
```bash
git clone https://github.com/your-repo/school-booking.git
cd school-booking
```
*Translation: "Download the files and go into the folder"*

### Step 2: Create a Virtual Space
We don't want to mess up your computer, so we make a "sandbox" for our app.
```bash
python -m venv .venv
```
*Translation: "Make a safe box called .venv"*

### Step 3: Turn on the Sandbox
**Windows**:
```bash
.venv\Scripts\Activate.ps1
```
**Mac/Linux**:
```bash
source .venv/bin/activate
```
*Translation: "Step inside the safe box"*

### Step 4: Install Parts
```bash
pip install -r requirements.txt
```
*Translation: "Download all the plugins and libraries we need"*

---

## Part 3: Configuration (The Settings)

We need to set some secret passwords.

1. Create a file called `.env`
2. Paste this inside:
```env
SECRET_KEY=my-secret-password
MAIL_USERNAME=greenwoodinternationaluk@gmail.com
MAIL_PASSWORD=ridw cmtm exwe khjl
DATABASE_URL=sqlite:///booking_system_v2.db
```
*Translation: "Here are the keys to the email and database"*

---

## Part 4: Running It! (Start the Engine)

1. **Create the Database**:
```bash
python populate_db.py
```
*Translation: "Build the filing cabinets and fill them with sample data"*
*(This creates admin, parents, tutors, and activities automatically!)*

2. **Start the Server**:
```bash
python app.py
```
*Translation: "Turn on the website"*

3. **Open in Browser**:
Go to: `http://127.0.0.1:5000`

---

## Part 5: How to Use It (User Manual)

### Login Details (Demo Accounts)

**1. The Admin (The Boss)**
- **Email**: `greenwoodinternationaluk@gmail.com`
- **Password**: `sanchitkaushal`
- **What to do**: Go to `/admin/login`. Create new activities!

**2. The Parent (The Customer)**
- **Email**: `parent@demo.com`
- **Password**: `demo123`
- **What to do**: Go to `/login`. Book a class! Download invoice!

**3. The Tutor (The Teacher)**
- **Email**: `sarah.smith@greenwood.edu`
- **Password**: `tutor123`
- **What to do**: Go to `/tutor/login`. Mark attendance!

---

## Troubleshooting (Fixing Problems)

**Problem**: "It says 'Module not found'!"
**Fix**: You forgot to activate the sandbox (Step 3) or install parts (Step 4).

**Problem**: "Email not sending!"
**Fix**: Check your internet. Check the `.env` file has the right password.

**Problem**: "Database is locked!"
**Fix**: Close the app and restart it.

---

**Ready to go? Start at Step 1!**
