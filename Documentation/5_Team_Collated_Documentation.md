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

We divided the work so everyone had a special technical job.

### 1. Sanchit Kaushal (The Leader & Guard)
**Role**: Security & Admin
- **Analogy**: He built the building, the locks on the doors, and the manager's office.
- **Key Jobs**:
  - Login system (Who are you?)
  - Security (Keep hackers out)
  - Admin Panel (Control room)
  - Putting it on the internet

### 2. Chichebendu Blessed Umeh (The Messenger)
**Role**: Emails & Integration
- **Analogy**: He is the postman and the secretary.
- **Key Jobs**:
  - Sending confirmation emails
  - Creating PDF invoices
  - Making calendar invites
  - Teacher's portal

### 3. Shiva Kasula (The Brain)
**Role**: Database & Logic
- **Analogy**: He is the filing clerk and the bouncer.
- **Key Jobs**:
  - Database (Storing info)
  - Rules (No double bookings!)
  - Waitlist (The queue)
  - Payments (The cash register)

### 4. Mohd Sharjeel (The Optimizer)
**Role**: Integration & Performance Engineer
- **Analogy**: He built the connections and made everything faster.
- **Key Jobs**:
  - **AJAX Integration**: Real-time updates without page refresh
  - **Performance Optimization**: Query optimization, caching, lazy loading
  - **Availability Algorithm**: Real-time calculation of remaining spots
  - **Client-Side Validation**: Input checking algorithms

---

## How It All Works Together

**Follow the Journey of a Booking**:

**Step 1: The Interface (Sharjeel's Code)**
- Parent visits website.
- Sharjeel's **responsive logic** detects a mobile phone.
- Sharjeel's **Jinja2 code** loops through activities and renders them.
- It shows "Swimming" with a Green "Available" badge (Logic-based).

**Step 2: The Login (Sanchit's Work)**
- Parent clicks "Login".
- Types password.
- Sanchit's security checks the password hash.
- Access Granted!

**Step 3: The Booking (Shiva's Work)**
- Parent clicks "Book Swimming".
- Shiva's logic checks: "Is it full?", "Did they pay?"
- Everything OK? -> Save to Database.

**Step 4: The Confirmation (Chichebendu's Work)**
- Immediately, an email is sent.
- "Ding!" Phone buzzes.
- PDF Invoice attached.
- Calendar event added to phone.

**Step 5: The Class (Everyone)**
- Teacher logs in (Sanchit)
- Checks list (Shiva)
- Marks attendance (Chichebendu)
- On a structured interface (Sharjeel)

---

## Technologies We Used (The Tools)

| Tool | What It Is | Why We Used It |
|------|------------|----------------|
| **Python** | Programming Language | Easy to write, powerful |
| **Flask** | Web Framework | Builds websites fast |
| **SQLite** | Database | Stores our data simply |
| **Jinja2** | Template Engine | Logic for HTML (Loops/Ifs) |
| **CSS3** | Styling Language | Layout and Design Architecture |
| **Git** | Version Control | Lets us work together without overwriting |

---

## Challenges We Solved

**Problem 1: Double Booking**
- *Scenario*: Two parents try to book the LAST spot at the exact same second.
- *Solution (Shiva)*: "Database Transactions". The computer freezes for 0.01 seconds, lets one in, and tells the other "Sorry, full!".

**Problem 2: Emails going to Spam**
- *Scenario*: Emails looked fake, so Gmail blocked them.
- *Solution (Chichebendu)*: Used professional SMTP settings and proper HTML templates. Now they hit the Inbox every time.

**Problem 3: Hackers**
- *Scenario*: Bad people trying to fake forms.
- *Solution (Sanchit)*: CSRF Tokens. Secret codes on every form that hackers can't guess.

**Problem 4: Code Maintainability**
- *Scenario*: Changing the theme color required editing 50 files.
- *Solution (Sharjeel)*: "CSS Variables Architecture". Defined colors in one place, used everywhere. Changed 50 files to 1 line of code.

---

## Conclusion

We built a professional, secure, and beautiful system. It solves a real problem for schools (messy paper forms) and makes life easier for parents, teachers, and admins.

**Project Status**: ✅ Complete & Ready for Use!
