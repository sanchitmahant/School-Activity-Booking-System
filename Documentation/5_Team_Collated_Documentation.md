# Team Collated Documentation
**Project**: School Activity Booking System  
**Team**: Sanchit, Chichebendu, Shiva, Sharjeel

---

## The Big Picture - What We Built

We built a complete **School Activity Booking Website**.

**Imagine Amazon, but for School Clubs**:
- Parents can shop for clubs (Swimming, Math, Art)
- They add to cart and pay
- They get receipts and calendar invites
- Teachers get class lists
- Admins manage everything

---

## Who Did What? (The Dream Team)

We divided the work so everyone had a special job.

### 1. Sanchit Kaushal (The Messenger)
**Role**: Email & Integration Specialist
- **Analogy**: He is the postman and the secretary.
- **Key Jobs**:
  - Sending confirmation emails
  - Creating PDF invoices
  - Making calendar invites
  - Tutor Portal (Teacher's View)

### 2. Chichebendu Blessed Umeh (The Guard)
**Role**: Security & Admin Specialist
- **Analogy**: He built the building, the locks on the doors, and the manager's office.
- **Key Jobs**:
  - Login system (Who are you?)
  - Security (Keep hackers out)
  - Admin Panel (Control room)
  - Putting it on the internet

### 3. Shiva Kasula (The Brain)
**Role**: Database & Logic
- **Analogy**: He is the filing clerk and the bouncer.
- **Key Jobs**:
  - Database (Storing info)
  - Rules (No double bookings!)
  - Waitlist (The queue)
  - Payments (The cash register)

### 4. Mohd Sharjeel (The Registrar)
**Role**: Backend & Attendance Specialist
- **Analogy**: He keeps the official records and checks safety.
- **Key Jobs**:
  - Attendance System (Who is present?)
  - Parent Portal (Dashboard logic)
  - Requirements (The Blueprints)
  - Testing (Finding bugs)

---

## How It All Works Together

**Follow the Journey of a Booking**:

**Step 1: The Visit (Sharjeel's Work)**
- Parent visits website.
- Sharjeel's requirements ensured it loads fast.
- Parent logs in to see their personal dashboard (Sharjeel's logic).

**Step 2: The Login (Chichebendu's Work)**
- Parent clicks "Login".
- Types password.
- Chichebendu's security checks the password hash.
- Access Granted!

**Step 3: The Booking (Shiva's Work)**
- Parent clicks "Book Swimming".
- Shiva's logic checks: "Is it full?", "Did they pay?"
- Everything OK? -> Save to Database.

**Step 4: The Confirmation (Sanchit's Work)**
- Immediately, an email is sent.
- "Ding!" Phone buzzes.
- PDF Invoice attached.
- Calendar event added to phone.

**Step 5: The Class (Everyone)**
- Teacher logs in (Chichebendu)
- Checks list (Shiva)
- Marks attendance (Sharjeel)
- On the Tutor Portal (Sanchit)

**Step 6: The Cancellation (Optional)**
- Parent clicks "Cancel Booking".
- **System Action**:
  - Removes booking from database.
  - **Instantly notifies** Parent (Confirmation email).
  - **Instantly notifies** Admin (Record update).
  - **Instantly notifies** Tutor (Class list update).
  - *Automatic Waitlist Promotion*: If someone was waiting, they get the spot automatically!

---

## Technologies We Used (The Tools)

| Tool | What It Is | Why We Used It |
|------|------------|----------------|
| **Python** | Programming Language | Easy to write, powerful |
| **Flask** | Web Framework | Builds websites fast |
| **SQLite** | Database | Stores our data simply |
| **HTML/CSS** | Design Code | Makes it look good |
| **Git** | Version Control | Lets us work together without overwriting |

---

## Challenges We Solved

**Problem 1: Double Booking**
- *Scenario*: Two parents try to book the LAST spot at the exact same second.
- *Solution (Shiva)*: "Database Transactions". The computer freezes for 0.01 seconds, lets one in, and tells the other "Sorry, full!".

**Problem 2: Emails going to Spam**
- *Scenario*: Emails looked fake, so Gmail blocked them.
- *Solution (Sanchit)*: Used professional SMTP settings and proper HTML templates. Now they hit the Inbox every time.

**Problem 3: Hackers**
- *Scenario*: Bad people trying to fake forms.
- *Solution (Chichebendu)*: CSRF Tokens. Secret codes on every form that hackers can't guess.

**Problem 4: Tracking Attendance**
- *Scenario*: Teachers were using paper lists and losing them.
- *Solution (Sharjeel)*: Built a digital attendance system that saves instantly to the database.

---

## Conclusion

We built a professional, secure, and beautiful system. It solves a real problem for schools (messy paper forms) and makes life easier for parents, teachers, and admins.

**Project Status**: ✅ Complete & Ready for Use!
