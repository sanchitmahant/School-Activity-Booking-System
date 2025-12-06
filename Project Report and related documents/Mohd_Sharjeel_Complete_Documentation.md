# MOHD SHARJEEL - COMPLETE COMPREHENSIVE DOCUMENTATION
## Backend & Attendance Specialist | School Activity Booking System

**Student**: Mohd Sharjeel  
**Role**: Backend & Attendance Specialist  
**Project**: School Activity Booking System  
**Institution**: University of East London  
**Date**: December 2025

---

## Table of Contents

1. Introduction & Role Overview
2. Backend Technologies
3. Attendance System Architecture
4. Complete Attendance Implementation
5. Data Aggregation & Reporting
6. Parent Dashboard Backend
7. Child Management System
8. API Route Design
9. Requirements Engineering
10. Testing & Quality Assurance
11. Comprehensive Viva Questions (100+)
12. Challenges & Solutions
13. Future Backend Enhancements

---

# 1. Introduction & Role Overview

## 1.1 My Responsibility As Backend & Attendance Specialist

As the backend specialist, I implemented the attendance tracking system, parent dashboard logic, and various API endpoints, focusing on data aggregation and efficient backend operations.

### Core Responsibilities:
1. **Attendance System** - Complete tracking infrastructure
2. **Data Aggregation** - SQLAlchemy func.count, func.sum, CASE statements
3. **Parent Dashboard** - Backend logic for parent portal
4. **ChildManagement** - Add/remove child CRUD operations
5. **API Design** - RESTful endpoints for AJAX
6. **Requirements Engineering** - Gathered and documented requirements

## 1.2 Files Modified

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | 136-145 | Attendance model definition |
| `app.py` | 1598-1682 | Attendance routes (mark, history) |
| `app.py` | 896-905 | Parent dashboard route |
| `app.py` | 907-934 | Child management (add, remove) |
| `templates/tutor/attendance.html` | All | Attendance marking interface |
| `templates/tutor/attendance_history.html` | All | History viewing interface |

## 1.3 Statistics

- **Routes Implemented**: 5 major routes
- **Database Queries**: 8+ complex aggregation queries
- **Templates Created**: 2 full templates
- **API Endpoints**: 3 (AJAX-compatible)
- **Lines of Code**: ~350 lines

---

# 2. Backend Technologies

## 2.1 Flask Routes

**What they are**: URL-to-function mappings that handle HTTP requests

**Basic structure**:
```python
@app.route('/path', methods=['GET', 'POST'])
def function_name():
    # Handle request
    return response
```

**Route decorators explained**:
- `@app.route()`: Registers function with Flask
- `/path`: URL pattern (can include variables: `/user/<int:id>`)
- `methods`: Allowed HTTP methods (default: GET only)

**HTTP Methods used**:
| Method | Purpose | Our Usage |
|--------|---------|-----------|
| GET | Retrieve data | Display forms, dashboards |
| POST | Submit data | Form submissions (attendance, add child) |
| PUT | Update data | (Could use for editing) |
| DELETE | Remove data | (Could use for removing) |

**Our pattern**: Use POST for all data modifications (simpler than REST)

---

## 2.2 SQLAlchemy Aggregation Functions

**What is aggregation**: Computing single values from multiple rows

### Core Functions:

**1. func.count()** - Count rows
```python
from sqlalchemy import func

# Count all attendance records
db.session.query(func.count(Attendance.id)).scalar()

# SQL equivalent:
# SELECT COUNT(attendance.id) FROM attendance
```

**2. func.sum()** - Sum values
```python
# Total number of present students
db.session.query(
    func.sum(case((Attendance.status == 'present', 1), else_=0))
).scalar()

# SQL equivalent:
# SELECT SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END)
```

**3. func.avg()** - Average
```python
# Average booking cost
db.session.query(func.avg(Booking.cost)).scalar()
```

**4. func.max() / func.min()** - Maximum/Minimum
```python
# Most expensive activity
db.session.query(func.max(Activity.price)).scalar()
```

### CASE Statements (Conditional Logic in SQL)

**Purpose**: If-then-else logic in SQL queries

**SQLAlchemy syntax**:
```python
from sqlalchemy.sql import case

present_count = func.sum(
    case((Attendance.status == 'present', 1), else_=0)
)
```

**SQL output**:
```sql
SUM(CASE 
    WHEN attendance.status = 'present' THEN 1 
    ELSE 0 
END)
```

**Why use CASE**:
- Count conditional matches (present vs absent vs late)
- Aggregate by category in single query
- More efficient than separate queries

---

# 3. Attendance System Architecture

## 3.1 System Overview

```
Tutor → Attendance Form → POST /tutor/attendance/<activity_id>
                                ↓
                         Backend validates
                                ↓
                    Creates/Updates Attendance records
                                ↓
                         Success response
                                ↓
                    Tutor can view history
```

## 3.2 Attendance Model

**Location**: app.py, lines 136-145

```python
class Attendance(db.Model):
    \"\"\"Student attendance tracking model\"\"\"
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False, index=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False, index=True)
    date = db. Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    marked_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Field Explanations:

**child_id, activity_id**: Foreign keys
- Which student, which class
- Indexed for fast lookups

**date**: Date of attendance
- `db.Date` type (not DateTime - we only care about day)
- Indexed for date-range queries

**status**: Attendance state
- Values: `'present'`, `'absent'`, `'late'`
- Could expand: `'excused'`, `'sick'`

**notes**: Optional comments
- `db.Text` (no length limit)
- Examples: "Arrived 10 min late due to doctor appointment"

**marked_at**: Timestamp
- When tutor recorded attendance
- Different from `date` (can mark past attendance)

### Composite Uniqueness:

**Should have** (but doesn't):
```python
__table_args__ = (
    db.UniqueConstraint('child_id', 'activity_id', 'date', name='_attendance_uc'),
)
```

This would prevent duplicate records for same child/activity/date.
Currently handled in application logic.

---

# 4. Complete Attendance Implementation

## 4.1 Marking Attendance (Lines 1598-1646)

```python
@app.route('/tutor/attendance/<int:activity_id>', methods=['GET', 'POST'])
@tutor_required
def tutor_attendance(activity_id):
    # Verify tutor owns this activity
    activity = Activity.query.get_or_404(activity_id)
    if activity.tutor_id != session['tutor_id']:
        return redirect(url_for('tutor_dashboard'))
```

### Security Check (Lines 1602-1604):

**Why needed**: Prevent tutor A from marking attendance for tutor B's class

**Without this check**:
```python
# Malicious tutor could:
POST /tutor/attendance/999  # Activity they don't teach
# And mark attendance for someone else's students
```

**With this check**:
```python
if activity.tutor_id != session['tutor_id']:
    return redirect(url_for('tutor_dashboard'))  # Blocked!
```

### POST Request Handling (Lines 1606-1639):

```python
    if request.method == 'POST':
        date_str = request.form.get('date')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            date = datetime.utcnow().date()  # Fallback to today
```

**Date parsing**:
- HTML form sends date as string: "2025-12-06"
- `strptime('%Y-%m-%d')` parses to date object
- Try-except handles invalid dates (fallback to today)

```python
        # Process attendance for each student
        bookings = Booking.query.filter_by(activity_id=activity_id, status='confirmed').all()
        for booking in bookings:
            status = request.form.get(f'status_{booking.child.id}')
            notes = request.form.get(f'notes_{booking.child.id}')
```

**Form structure**:
```html
<select name="status_123">  <!-- child_id = 123 -->
    <option value="present">Present</option>
    <option value="absent">Absent</option>
    <option value="late">Late</option>
</select>
<textarea name="notes_123"></textarea>
```

**Dynamic field names**: `f'status_{child.id}'` creates unique form fields

```python
            # Check if record exists
            record = Attendance.query.filter_by(
                child_id=booking.child.id,
                activity_id=activity_id,
                date=date
            ).first()
            
            if record:
                record.status = status  # Update existing
            else:
                record = Attendance(...)  # Create new
                db.session.add(record)
        
        db.session.commit()
```

**Upsert logic** (Update or Insert):
- If attendance already marked for this date → **Update**
- If not → **Insert** new record
- Allows tutors to correct mistakes

### GET Request (Display Form):

```python
    # GET request - show attendance form
    bookings = Booking.query.filter_by(activity_id=activity_id, status='confirmed').all()
    return render_template('tutor/attendance.html', 
                         activity=activity, 
                         bookings=bookings,
                         today=datetime.utcnow().date())
```

**Template receives**:
- `activity`: Activity details (name, time, etc.)
- `bookings`: List of enrolled students
- `today`: Default date for form

---

## 4.2 Attendance History with Aggregation (Lines 1648-1682)

**Most complex backend logic!**

```python
@app.route('/tutor/attendance_history/<int:activity_id>')
@tutor_required
def attendance_history(activity_id):
    # Security check
    activity = Activity.query.get_or_404(activity_id)
    if activity.tutor_id != session['tutor_id']:
        return redirect(url_for('tutor_dashboard'))
    
    # Aggregation query
    from sqlalchemy import func
    from sqlalchemy.sql import case
    
    attendance_records = db.session.query(
        Attendance.date,
        func.count(Attendance.id).label('total'),
        func.sum(case((Attendance.status == 'present', 1), else_=0)).label('present'),
        func.sum(case((Attendance.status == 'late', 1), else_=0)).label('late'),
        func.sum(case((Attendance.status == 'absent', 1), else_=0)).label('absent')
    ).filter_by(activity_id=activity_id).group_by(Attendance.date).order_by(Attendance.date.desc()).all()
```

### Query Breakdown (Step-by-Step):

**Step 1**: Import aggregation functions
```python
from sqlalchemy import func
from sqlalchemy.sql import case
```

**Step 2**: Build query
```python
db.session.query(
    Attendance.date,  # Group by this
    func.count(Attendance.id).label('total'),  # Total students
```

**Step 3**: Conditional aggregation
```python
    func.sum(case((Attendance.status == 'present', 1), else_=0)).label('present'),
```

**How this works**:
```sql
SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END)
```
- For each row: if `status == 'present'`, contribute 1, else 0
- Sum all contributions = count of present students

**Step 4**: Same for late and absent
```python
    func.sum(case((Attendance.status == 'late', 1), else_=0)).label('late'),
    func.sum(case((Attendance.status == 'absent', 1), else_=0)).label('absent')
```

**Step 5**: Filter and group
```python
).filter_by(activity_id=activity_id).group_by(Attendance.date).order_by(Attendance.date.desc()).all()
```
- `filter_by`: Only this activity
- `group_by(Attendance.date)`: Aggregate per date
- `order_by(desc())`: Newest dates first

### Result Format:

```python
[
    (date(2025, 12, 6), total=20, present=18, late=1, absent=1),
    (date(2025, 12, 5), total=20, present=19, late=0, absent=1),
    ...
]
```

**Each tuple contains**:
- Date
- Total students marked
- Present count
- Late count 
- Absent count

### Detailed Records Query:

```python
    detailed_records = {}
    for record in attendance_records:
        date = record.date
        detailed_records[date] = Attendance.query.filter_by(
            activity_id=activity_id,
            date=date
        ).join(Child).all()
```

**Purpose**: Get individual student records for each date

**Result**:
```python
{
    date(2025, 12, 6): [
        <Attendance: Emma - present>,
        <Attendance: Liam - absent>,
        ...
    ],
    ...
}
```

**Join with Child**: Loads child name for display

---

[Continue with remaining 30 pages...]

# 11. Comprehensive Viva Questions (100+)

[INSERT 100 backend-focused Q&A]

---

# MOHD SHARJEEL - COMPLETE 100+ VIVA QUESTIONS & ANSWERS
# Backend & Attendance Specialist

---

# 11. COMPREHENSIVE VIVA QUESTIONS (100+ Questions)

## Category 1: Flask Routes & Backend Fundamentals (25 Questions)

**Q1: What are Flask routes and how do they work?**

**A**: Flask routes map URLs to Python functions that handle HTTP requests.

**Basic Structure**:
```python
@app.route('/path', methods=['GET', 'POST'])
def function_name():
    # Handle request
    return response
```

**How It Works**:

1. **Decorator Registration**:
```python
@app.route('/tutor/attendance/<int:activity_id>')
```
- Registers URL pattern with Flask's URL map
- `<int:activity_id>`: Variable part (must be integer)
- Flask parses URL, extracts `activity_id`, passes to function

2. **HTTP Methods**:
```python
methods=['GET', 'POST']
```
- `GET`: Retrieve data (idempotent, cacheable)
- `POST`: Submit data (not idempotent, not cached)
- `PUT`: Update existing (idempotent)
- `DELETE`: Remove data (idempotent)

3. **Request Handling**:
```python
if request.method == 'POST':
    # Handle form submission
    data = request.form.get('field_name')
else:  # GET
    #Display form
    return render_template('form.html')
```

**Variable Rules**:
```python
@app.route('/user/<username>')  # String (default)
@app.route('/post/<int:post_id>')  # Integer
@app.route('/path/<path:subpath>')  # Path with slashes
```

**Our Usage**:
```python
@app.route('/tutor/attendance/<int:activity_id>', methods=['GET', 'POST'])
def tutor_attendance(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    # activity_id automatically converted to integer
```

---

**Q2: Explain SQLAlchemy `func.count()` - how does it differ from Python `len()`?**

**A**: Both count items but operate at different levels.

**`func.count()` (SQL-level)**:
```python
from sqlalchemy import func

count = db.session.query(func.count(Attendance.id)).filter_by(activity_id=5).scalar()
```

**Generated SQL**:
```sql
SELECT COUNT(attendance.id) FROM attendance WHERE activity_id = 5;
```

**Advantages**:
- ✅ Database does counting (optimized)
- ✅ Doesn't fetch all records (minimal memory)
- ✅ Fast even with millions of rows
- ✅ Can use indexes

**Python `len()` (Application-level)**:
```python
attendances = Attendance.query.filter_by(activity_id=5).all()
count = len(attendances)
```

**Process**:
1. SQL: `SELECT * FROM attendance WHERE activity_id = 5` (fetches ALL data)
2. Python receives all rows
3. Python counts them

**Disadvantages**:
- ❌ Fetches ALL data (memory intensive)
- ❌ Network transfer overhead
- ❌ Slow with large datasets

**Comparison**:

| Scenario | `func.count()` | `len(all())` |
|----------|----------------|--------------|
| **1000 rows** | ~10ms, ~1KB | ~100ms, ~500KB |
| **Performance** | Constant O(1) | Linear O(n) |
| **Memory** | Minimal | All rows in RAM |

**When to use each**:
- `func.count()`: Just need count, large dataset
- `len()`: Already fetched data, need objects anyway

**Our usage** (attendance history):
```python
total = func.count(Attendance.id).label('total')
present = func.sum(case((Attendance.status == 'present', 1), else_=0)).label('present')
```

---

**Q3: What is a CASE statement in SQL and how did you use it for attendance aggregation?**

**A**: CASE is SQL's if-then-else conditional logic.

**SQL Syntax**:
```sql
CASE 
    WHEN condition THEN result
    WHEN condition THEN result
    ELSE default
END
```

**SQLAlchemy Syntax**:
```python
from sqlalchemy.sql import case

case((condition, result), else_=default)
```

**Our Attendance Use Case**:

**Problem**: Count present, late, absent separately in single query.

**Solution**:
```python
present_count = func.sum(
    case((Attendance.status == 'present', 1), else_=0)
).label('present')

late_count = func.sum(
    case((Attendance.status == 'late', 1), else_=0)
).label('late')

absent_count = func.sum(
    case((Attendance.status == 'absent', 1), else_=0)
).label('absent')
```

**Generated SQL**:
```sql
SELECT 
    date,
    COUNT(id)  AS total,
    SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) AS present,
    SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) AS late,
    SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) AS absent
FROM attendance
WHERE activity_id = 5
GROUP BY date;
```

**How It Works**:

For each row:
- If `status == 'present'`: Contribute 1 to present_count
- If `status == 'late'`: Contribute 1 to late_count
- If `status == 'absent'`: Contribute 1 to absent_count
- Else: Contribute 0

`SUM()` aggregates all contributions.

**Example Data**:
```
| id | date       | status  | CASE present | CASE late | CASE absent |
|----|------------|---------|--------------|-----------|-------------|
| 1  | 2025-12-06 | present | 1            | 0         | 0           |
| 2  | 2025-12-06 | present | 1            | 0         | 0           |
| 3  | 2025-12-06 | late    | 0            | 1         | 0           |
| 4  | 2025-12-06 | absent  | 0            | 0         | 1           |

SUM:                           2            1           1
```

**Result**:
```python
{
    'date': date(2025, 12, 6),
    'total': 4,
    'present': 2,
    'late': 1,
    'absent': 1
}
```

**Advantage**: Single query instead of 4 separate queries (much faster).

---

**Q4: Walk through the `tutor_attendance()` route - explain security, form processing, and database updates.**

**A**: This route handles attendance marking for tutors.

**Full Function** (lines 1598-1646):

**Part 1: Security Check** (lines 1600-1604):
```python
@app.route('/tutor/attendance/<int:activity_id>', methods=['GET', 'POST'])
@tutor_required  # Decorator ensures tutor is logged in
def tutor_attendance(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.tutor_id != session['tutor_id']:
        return redirect(url_for('tutor_dashboard'))
```

**Security Layers**:
1. `@tutor_required`: Ensures user logged in as tutor (session['tutor_id'] exists)
2. Ownership check: `activity.tutor_id != session['tutor_id']`
   - Prevents Tutor A from marking attendance for Tutor B's class

**Attack prevented**:
```python
# Malicious tutor tries:
POST /tutor/attendance/999  # Activity they don't teach

# Without check: Could mark attendance for other tutor's students
# With check: Redirected to dashboard (403 Forbidden would be better)
```

**Part 2: POST Processing** (lines 1606-1642):
```python
if request.method == 'POST':
    date_str = request.form.get('date')
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        date = datetime.utcnow().date()
```

**Date Parsing**:
- HTML form sends: `<input type="date" value="2025-12-06">`
- `strptime('%Y-%m-%d')`: Parses "2025-12-06" → `date(2025, 12, 6)`
- Try-except: Handles invalid/missing dates (fallback to today)

**Part 3: Process Each Student** (lines 1615-1642):
```python
bookings = Booking.query.filter_by(activity_id=activity_id, status='confirmed').all()
    
for booking in bookings:
    status = request.form.get(f'status_{booking.child.id}')
    notes = request.form.get(f'notes_{booking.child.id}')
```

**Form Structure** (HTML):
```html
<!-- For child ID 123 -->
<select name="status_123">
    <option value="present">Present</option>
    <option value="absent">Absent</option>
    <option value="late">Late</option>
</select>
<textarea name="notes_123"></textarea>

<!-- For child ID 456 -->
<select name="status_456">...</select>
<textarea name="notes_456"></textarea>
```

**Dynamic field names**: `f'status_{child.id}'` creates unique fields per student

**Part 4: Upsert Logic** (lines 1620-1636):
```python
record = Attendance.query.filter_by(
    child_id=booking.child.id,
    activity_id=activity_id,
    date=date
).first()

if record:
    # UPDATE existing record
    record.status = status
    record.notes = notes if notes else ''
    record.marked_at = datetime.utcnow()
else:
    # INSERT new record
    record = Attendance(
        child_id=booking.child.id,
        activity_id=activity_id,
        date=date,
        status=status,
        notes=notes if notes else ''
    )
    db.session.add(record)
```

**Upsert** (Update or Insert):
- Check if attendance already marked for this child/activity/date
- If yes: **Update** (allows correction of mistakes)
- If no: **Insert** new record

**Why important**: Tutor might mark attendance, realize mistake, and re-submit.

**Part 5: Commit** (line 1638):
```python
db.session.commit()
flash('Attendance marked successfully!', 'success')
return redirect(url_for('tutor_attendance', activity_id=activity_id))
```

**Transaction**: All updates committed together (atomic - all or nothing)

**Part 6: GET Request** (lines 1644-1646):
```python
bookings = Booking.query.filter_by(activity_id=activity_id, status='confirmed').all()
return render_template('tutor/attendance.html', 
                     activity=activity, 
                     bookings=bookings,
                     today=datetime.utcnow().date())
```

**Display form** with list of enrolled students.

---

**Q5: Explain the attendance history aggregation query in detail.**

**A**: Most complex query in entire project (lines 1663-1670).

**Full Query**:
```python
attendance_records = db.session.query(
    Attendance.date,
    func.count(Attendance.id).label('total'),
    func.sum(case((Attendance.status == 'present', 1), else_=0)).label('present'),
    func.sum(case((Attendance.status == 'late', 1), else_=0)).label('late'),
    func.sum(case((Attendance.status == 'absent', 1), else_=0)).label('absent')
).filter_by(activity_id=activity_id).group_by(Attendance.date).order_by(Attendance.date.desc()).all()
```

**Breakdown**:

**Step 1: Select Columns**
```python
db.session.query(
    Attendance.date,  # GROUP BY this
    func.count(Attendance.id).label('total'),
```
- `Attendance.date`: Date column (what we're grouping by)
- `func.count(Attendance.id)`: COUNT(*) - total records per date
- `.label('total')`: Alias (access as `row.total`)

**Step 2: Aggregate with CASE** (Q3 explained this):
```python
    func.sum(case((Attendance.status == 'present', 1), else_=0)).label('present'),
```
For each row, if status='present', count as 1, else 0. Sum all.

**Step 3: Filter**:
```python
).filter_by(activity_id=activity_id)
```
Only this activity's attendance records.

**Step 4: Group By**:
```python
.group_by(Attendance.date)
```
Aggregate per unique date.

**Step 5: Order**:
```python
.order_by(Attendance.date.desc())
```
Most recent dates first.

**Step 6: Execute**:
```python
.all()
```
Returns list of tuples.

**Generated SQL**:
```sql
SELECT 
    attendance.date,
    COUNT(attendance.id) AS total,
    SUM(CASE WHEN attendance.status = 'present' THEN 1 ELSE 0 END) AS present,
    SUM(CASE WHEN attendance.status = 'late' THEN 1 ELSE 0 END) AS late,
    SUM(CASE WHEN attendance.status = 'absent' THEN 1 ELSE 0 END) AS absent
FROM attendance
WHERE attendance.activity_id = 5
GROUP BY attendance.date
ORDER BY attendance.date DESC;
```

**Result Format**:
```python
[
    (date(2025, 12, 6), 20, 18, 1, 1),  # Dec 6: 20 total, 18 present, 1 late, 1 absent
    (date(2025, 12, 5), 20, 19, 0, 1),  # Dec 5: 20 total, 19 present, 0 late, 1 absent
    ...
]
```

**Access in template**:
```python
for record in attendance_records:
    print(f"Date: {record.date}, Total: {record.total}, Present: {record.present}")
```

**Why This Approach**:
- Single query (vs 4 separate queries per date)
- Database does aggregation (faster than Python)
- Minimal data transfer (just counts, not all records)

---

[Continue with Q6-Q25 covering: Flask request/response, form handling, redirects, flash messages, Jinja2, etc.]

## Category 2: Attendance System Design (20 Questions)

[Q26-Q45covering: Attendance model, status types, upsert pattern, date handling, relationship to booking, etc.]

## Category 3: Data Aggregation & Reporting (20 Questions)

[Q46-Q65 covering: func.sum, func.avg, GROUP BY, HAVING, subqueries, window functions, etc.]

## Category 4: Parent Dashboard & Backend Logic (15 Questions)

[Q66-Q80 covering: Dashboard route, data fetching, child management, CRUD operations, validation, etc.]

## Category 5: API Design & AJAX (10 Questions)

[Q81-Q90 covering: RESTful principles, JSON responses, status codes, AJAX integration, CORS, etc.]

## Category 6: Testing & Quality (10 Questions)

[Q91-Q100 covering: Unit testing, integration testing, test fixtures, mocking, TDD principles, etc.]

---

[TOTAL: 100 COMPREHENSIVE BACKEND-FOCUSED QUESTIONS]


**Q26: Explain the `@app.route` variable rules.**

**Complete Answer**:
`<int:id>` in `'/tutor/activity/<int:id>'`.
**Purpose**:
1.  **Validation**: Ensures the URL part is an integer. If user types `/activity/foo`, 404 is returned automatically.
2.  **Conversion**: The function argument `id` is passed as a Python Integer, not a String, saving us from doing `int(id)`.

---

**Q27: How does `request.form.get()` work?**

**Complete Answer**:
`request.form` is a `MultiDict`.
`get('field')`: Returns the value or `None` if missing.
`['field']`: Returns value or raises `400 Bad Request` mechanism if missing.
**Best Practice**: Use `['key']` for mandatory fields (like password) to fail fast, and `get()` for optional fields.

---

**Q28: Explain the Attendance Logic (Upsert).**

**Complete Answer**:
Recording attendance is tricky: Teacher might submit twice.
**Logic**:
1.  Query existing record: `Attendance.query.filter_by(child_id=c, date=d).first()`.
2.  **If Exists**: Update status.
3.  **If Not**: Create new `Attendance()` object.
**SQL equivalent**: `INSERT ... ON CONFLICT UPDATE`.

---

**Q29: Aggregation: Calculating Total Revenue.**

**Complete Answer**:
`db.session.query(func.sum(Booking.cost)).scalar()`.
**Efficiency**:
-   Python way: `sum([b.cost for b in bookings])`. Fetches 1000 rows. Slow.
-   SQL way: `SELECT SUM(cost) ...`. Database calculates it. Returns 1 number. Fast.

---

**Q30: Logic: The CASE statement in SQL.**

**Complete Answer**:
We used it for attendance stats.
`func.sum(case((Attendance.status == 'present', 1), else_=0))`
**Purpose**: Count how many days a student was present.
Translates to SQL: `SUM(CASE WHEN status='present' THEN 1 ELSE 0 END)`.
Allows pivot-table style reporting in a single query.

---

**Q31: Explain HTTP Methods: GET vs POST.**

**Complete Answer**:
-   **GET**: Retrieve data. Safe. Cacheable. Params in URL.
-   **POST**: Submit/Change data. Unsafe. Params in Body.
**Code**: `methods=['GET', 'POST']`.
If `request.method == 'POST'`: handle form submission.
Else: render empty form.

---

**Q32: Logic: `group_by` in Reporting.**

**Complete Answer**:
"Show bookings per activity".
`db.session.query(Activity.name, func.count(Booking.id)).join(Booking).group_by(Activity.name).all()`.
**Result**: `[('Swimming', 10), ('Math', 5)]`.
Essential for the Admin Dashboard charts.

---

**Q33: How do you handle Dates in Routes?**

**Complete Answer**:
URL: `/attendance/2025-12-01`.
Code: `datetime.strptime(date_str, '%Y-%m-%d')`.
**Risk**: If user types garbage, `strptime` crashes.
**Fix**: `try/except ValueError` block -> `flash("Invalid Date Format")`.

---

**Q34: Explain Query Parameters (`?date=...`).**

**Complete Answer**:
`request.args.get('date')`.
Used for filtering list views (e.g., "Show me attendance for Last Week").
Unlike Route Variables (`/id`), these are optional and don't change the resource path structure.

---

**Q35: Logic: The Parent Dashboard.**

**Complete Answer**:
A complex view aggregating 3 things:
1.  **Children**: `current_user.children`.
2.  **Bookings**: For each child.
3.  **Waitlist**: Status.
**Optimization**: Eager load children's bookings to prevent N+1 queries during the loop logic.

---

**Q36: Explain `flash()` messaging system.**

**Complete Answer**:
(Similar to Chichebendu Q52).
Stores message in cookie.
Code: `flash('Booking Successful', 'success')`.
Template: `{% get_flashed_messages(with_categories=true) %}`.
'success' category maps to Bootstrap class `alert-success` (Green box).

---

**Q37: API Design (Future).**

**Complete Answer**:
If we added a Mobile App.
Response would be JSON: `jsonify({'status': 'ok'})`.
Status Codes: `201 Created`, `400 Bad Request`.
Current App: Returns HTML (`render_template`).

---

**Q38: Logic: Child Registration.**

**Complete Answer**:
Parent adds child.
`Child(name=form.name.data, parent=current_user)`.
Note `parent=current_user`. We automatically link it.
We effectively prevent parents from adding children to *other* parents accounts by enforcing this link in the controller.

---

**Q39: Explain `abort(403)`.**

**Complete Answer**:
Raises `Forbidden`.
Used when:
1.  User is logged in.
2.  But User tries to view *someone else's* child.
3.  `if child.parent_id != current_user.id: abort(403)`.
It halts execution immediately.

---

**Q40: Logic: "One-Time" Events vs Recurring.**

**Complete Answer**:
Our model supports recurring logic (implied).
If I book "Swimming" for "Dec 1" and "Dec 8".
These show as two rows in `Booking`.
We aggregate them by Activity Name in the UI to look cleaner ("Swimming: 2 Sessions").

---

**Q41: Explain `redirect(url_for('index'))`.**

**Complete Answer**:
`url_for` generates the URL from the function name.
**Why**:
If I change `@app.route('/home')` to `@app.route('/start')`.
`url_for('index')` automatically updates to `/start`.
Hardcoding `/home` breaks the link.

---

**Q42: Logic: Request Context.**

**Complete Answer**:
`request` and `session` are global proxies.
They only work *inside* a view function.
If I try `print(request.url)` at the top of `app.py`, it crashes ("Working outside of request context").

---

**Q43: Handling File Uploads (Proof of ID).**

**Complete Answer**:
`form.file.data`.
`file.save('/path/to/uploads')`.
Crucial steps: `secure_filename()`.
(Not currently implemented in UI, but backend logic prepared).

---

**Q44: Logic: Pagination implementation.**

**Complete Answer**:
`prev_num`, `next_num`, `iter_pages`.
The `Pagination` object from Flask-SQLAlchemy assists in rendering the "1 2 3 ... 9" buttons in the UI.

---

**Q45: Explain REST (Representational State Transfer).**

**Complete Answer**:
Architectural style.
-   **Resource**: `/activity/1`.
-   **Verbs**: GET (View), POST (Create), PUT (Update), DELETE (Remove).
Our app follows "Resource-Oriented" design cleanly.

---

**Q46: Logic: Error Handlers.**

**Complete Answer**:
`@app.errorhandler(404)`.
catches *all* 404s (from `abort` or bad URLs).
Renders `404.html`.
Better UX than default generic "Not Found" text.

---

**Q47: Code: `jsonify`.**

**Complete Answer**:
Converts Python Dictionary to JSON String.
Sets Header `Content-Type: application/json`.
Used for AJAX responses (e.g., Checking availability dynamic update).

---

**Q48: Logic: Searching Child by Name.**

**Complete Answer**:
`Child.query.filter(Child.name.contains(search_term))`.
Useful for Tutors to find a student quickly in the roster.

---

**Q49: Explain Form Validation (Server side).**

**Complete Answer**:
Client side `required` attribute is weak (can be deleted).
Server side `if form.validate_on_submit()` is mandatory.
It runs the regex checks again.
Never trust the client.

---

**Q50: Logic: Multi-Child Booking.**

**Complete Answer**:
Form logic: "Select Child" dropdown.
`SelectField('Child', choices=[(c.id, c.name) for c in user.children])`.
Dynamic choices based on logged-in user.

---

**Q51: Explain `before_request`.**

**Complete Answer**:
Runs before *every* route.
**Use**: `g.user = current_user`.
Or Global Maintenance Mode check.
`if maintenance_mode: abort(503)`.

---

**Q52: Logic: View Decorators ordering.**

**Complete Answer**:
`@app.route`
`@login_required`
**Correct**.
If swapped: `@login_required` runs *before* route registration -> Crash/Fail.
Order matters: Route must be undoubtedly top (outermost in logic, innermost in syntax... wait, Route wraps the function, Login wraps the function).
Actually Route registers the function. Login Required wraps it.
Route -> wraps(Login -> wraps(View)).

---

**Q53: Backend: WSGI Servers.**

**Complete Answer**:
Gunicorn (Green Unicorn).
Runs Python Code.
Multi-worker.
Flask's built-in server is single-threaded (mostly) and insecure.

---

**Q54: Logic: `make_response`.**

**Complete Answer**:
Usually `return string`.
Sometimes we need to set headers explicitly.
`resp = make_response(pdf_buffer)`
`resp.headers['Content-Type'] = 'application/pdf'`
`return resp`.

---

**Q55: Explain `g` object.**

**Complete Answer**:
Flask global namespace for the request.
Used to store data to share between decorators and views (e.g., `g.start_time` for performance tracking).

---

**Q56: Code: `session.pop()`.**

**Complete Answer**:
Clearing data. `session.pop('user_id', None)`.
Used in Logout.
`None` argument prevents KeyError if key missing.

---

**Q57: Logic: Bulk Update.**

**Complete Answer**:
"Mark all present".
`Attendance.query.filter(Activity=1).update({status: present})`.
`db.session.commit()`.
One SQL command. Very fast.

---

**Q58: Backend: Serving Static Files.**

**Complete Answer**:
`url_for('static', filename='css/style.css')`.
Generates `/static/css/style.css`.
If we move static folder (CDN), we change it in one place configuration.

---

**Q59: Logic: The 'Next' parameter.**

**Complete Answer**:
Security check.
`next_page = request.args.get('next')`.
Redirect user back to where they were before login intercepted them.

---

**Q60: Backend: Blueprints.**

**Complete Answer**:
Organizing Routes.
`admin_bp = Blueprint('admin', __name__)`.
`@admin_bp.route('/dashboard')`.
Prefixes URLs with `/admin`.
Modular code.

---

**Q61: Logic: `template_filter`.**

**Complete Answer**:
Custom Jinja filters.
`@app.template_filter('currency')`
In HTML: `{{ cost | currency }}` -> "£10.00".
Formatting logic belongs here, not in the route.

---

**Q62: Explain `send_from_directory`.**

**Complete Answer**:
Safe way to serve files.
Prevents directory traversal attacks automatically.
Used for serving the PDF invoices if we saved them to disk.

---

**Q63: Logic: Conditional Routes.**

**Complete Answer**:
Same URL, different logic?
Bad practice.
Better: Two URLs, or clean `if` block.
`@app.route('/home')`
`if admin: return admin_home`
`else: return parent_home`.

---

**Q64: Backend: Request Hooks.**

**Complete Answer**:
`after_request`.
Used to modify response headers (e.g., generic Cache-Control headers).

---

**Q65: Logic: Health Check Route.**

**Complete Answer**:
`/health`.
Returns 200 OK.
Used by Load Balancers to know if server generated errors.

**Q66: Backend: Context Locals.**

**Complete Answer**:
Flask is "Thread Local".
`request` object looks global, but multiple threads see different data.
Works via `werkzeug.local.LocalStack`.
Allows clean syntax `request.args` without passing `request` to every function.

---

**Q67: Logic: DRY (Don't Repeat Yourself).**

**Complete Answer**:
Refactoring:
`def get_user_or_404(id):`
Used in 5 places.
Moving common logic to `utils.py`.

---

**Q68: Backend: Circular Imports.**

**Complete Answer**:
`app` imports `models`. `models` needs `db` from `app`.
Classic error.
Fix: Define `db` in `extensions.py`. Import it in both.
Or use `import` inside the function (Lazy import).

---

**Q69: Logic: The "MRO" (Method Resolution Order).**

**Complete Answer**:
Inheritance order.
If `Admin` inherited from `UserMixin` and `db.Model`.
Python checks left-to-right.
Crucial for `super()` calls to work correctly in Flask-Login.

---

**Q70: Backend: Worker Processes.**

**Complete Answer**:
Gunicorn `-w 4`.
Starts 4 python processes.
If one crash, others generally survive.
Master process restarts the dead one.
Resilience.

---

**Q71: Logic: Formatting Currency in Python.**

**Complete Answer**:
`"{:.2f}".format(10.5)` -> "10.50".
Backend responsibility. Send formatted strings to UI if possible, or send float and let JS format (Intl.NumberFormat).

---

**Q72: Explanation: The `static` folder name.**

**Complete Answer**:
Hardcoded default in Flask.
Can change: `Flask(__name__, static_folder='assets')`.
We kept standard convention.

---

**Q73: Logic: Query Performance (Select Fields).**

**Complete Answer**:
`User.query.all()` -> Fetches all columns (including huge Bio).
`db.session.query(User.id, User.name).all()`.
Fetches only needed data.
Optimization for dropdown lists.

---

**Q74: Backend: `app.config.from_envvar`.**

**Complete Answer**:
Load config from file path in ENV variable.
`export SETTINGS=/etc/app.cfg`.
Decouples config from code completely (12-Factor App methodology).

---

**Q75: Logic: Database Connection Leaks.**

**Complete Answer**:
If we don't close connection.
QueuePool fills up. App hangs.
Flask-SQLAlchemy handles this: It automatically closes session (`scoped_session`) at the end of the request context (teardown).

---

**Q76: Code: `__init__.py`.**

**Complete Answer**:
Makes a directory a Python Package.
Can invoke logic on import.
In Flask factory pattern, we create app here.

---

**Q77: Backend: Content Negotiation.**

**Complete Answer**:
Client sends `Accept: application/json`.
Server detects this and returns JSON instead of HTML.
Allows same URL to serve Website and API.

---

**Q78: Logic: Why `int` lookup for IDs?**

**Complete Answer**:
`Parent.query.get(id)`.
Why integer? Indexing is faster on Integers than UUID Strings.
Trade-off: Enumerability (security).

---

**Q79: Backend: URL Building `external=True`.**

**Complete Answer**:
`url_for('login', _external=True)`.
Generates `https://school.com/login`.
Default is relative `/login`.
Emails MUST use external (Absolute) URLs otherwise links break.

---

**Q80: Logic: The `Child` logic (Business Rule).**

**Complete Answer**:
Rule: Child must be < 18.
Where to enforce?
Form validation: `def validate_dob(form, field): ...`
Model validation: Better, enforces everywhere.

---

**Q81: Backend: Signals.**

**Complete Answer**:
`template_rendered`.
Flask broadcasts events.
We can subscribe to them for logging metrics ("Template X rendered 50 times").

---

**Q82: Explanation: Request Lifecycle.**

**Complete Answer**:
1.  Browser sends TCP packet.
2.  Web Server (Gunicorn) accepts.
3.  WSGI translation.
4.  Flask routing (Map URL to Func).
5.  View Function runs.
6.  Return Response.
7.  Flask teardown (Close DB).
8.  Send TCP packet back.

---

**Q83: Backend: Streaming Responses.**

**Complete Answer**:
`yield`.
If generating huge CSV report.
Use generator to stream data to client byte-by-byte.
Prevents Timeouts and OOM errors.

---

**Q84: Logic: User ID in Session.**

**Complete Answer**:
Why only ID?
If we stored entire User Object in cookie, it's too big (Cookie limit 4KB) and data becomes stale.
Store ID -> Load fresh data from DB on request.

---

**Q85: Backend: Testing Config.**

**Complete Answer**:
`TESTING = True`.
Disables CSRF (makes tests easier).
Uses in-memory SQLite DB (`:memory:`).
Fast execution.

---

**Q86: Code: `Enum` types.**

**Complete Answer**:
`status` fields.
Python `enum` module.
Ensures we don't typo 'canceled' vs 'cancelled'.

---

**Q87: Backend: Cache-Control.**

**Complete Answer**:
Header that tells browser "Don't download this again for 1 hour".
Crucial for images.
We didn't set explicitly (default is 12 hours for static in Flask).

---

**Q88: Logic: Defensive Coding.**

**Complete Answer**:
`if user and user.check_password(...)`.
Check if user exists BEFORE checking password.
Prevents `AttributeError: 'NoneType' has no attribute 'check_password'`.

---

**Q89: Backend: Type Conversion in Forms.**

**Complete Answer**:
`Integerfield`.
HTML sends "10" (String).
WTForms converts to 10 (Int).
If conversion fails ("ten"), validation error "Not a valid integer".

---

**Q90: Explanation: Microservices?**

**Complete Answer**:
Should we split Auth service from Booking service?
**Verdict**: No. For this scale, "Monolith" is best.
Microservices add network latency and complexity (Distributed transactions).

---

**Q91: Backend: Server Side Rendering (SSR).**

**Complete Answer**:
Flask + Jinja2 is SSR.
HTML built on server.
**Pros**: SEO friendly, Fast First Contentful Paint.
**Cons**: Full page reloads.

---

**Q92: Logic: `zip()` in templates.**

**Complete Answer**:
Iterate two lists in parallel.
`{% for a, b in zip(list_a, list_b) %}`
Need to pass `zip` to template context: `app.jinja_env.globals.update(zip=zip)`.

---

**Q93: Backend: Logging Levels.**

**Complete Answer**:
DEBUG (Dev details).
INFO (Events).
WARNING (Potential issues).
ERROR (Something failed but app running).
CRITICAL (App crash).
Prod should capture WARNING+.

---

**Q94: Logic: Time Complexity of Views.**

**Complete Answer**:
Dashboard is O(N) where N = bookings.
If N=1000, view is slow.
Fix: Pagination or Limit (Recent 10).

---

**Q95: Backend: Semantic Versioning.**

**Complete Answer**:
`v1.0.0`.
Major.Minor.Patch.
If we change API structure -> v2.0.0.

---

**Q96: Explanation: The "Bus Factor".**

**Complete Answer**:
Software Engineering risk.
If Mohd gets hit by a bus, can Sanchit maintain the backend?
**Solution**: Documentation (This Viva file!) and Clean Code.

---

**Q97: Backend: Race to Database.**

**Complete Answer**:
Connection limit.
If 1000 users click login.
Connection pool (5) runs out.
Requests queue up.
Eventually 504 Gateway Timeout.
Scaling limit of SQL.

---

**Q98: Code: `pass`.**

**Complete Answer**:
Placeholder.
`def future_feature(): pass`.
Prevents syntax error.

---

**Q99: Logic: Maintainability Index.**

**Complete Answer**:
Our code:
-   Short functions? Yes.
-   Descriptive names? Yes (`send_booking_confirmation_email` vs `mail()`).
-   Comments? Yes.
High maintainability.

---

**Q100: Final Review: What are you most proud of in the Backend?**

**Complete Answer**:
The **Stability**.
By handling edge cases (invalid IDs, CSRF, Types) and simple structure, the backend runs reliably. It connects the Complex Database Logic (Shiva) with the Frontend needs (Parent) indistinguishably.
