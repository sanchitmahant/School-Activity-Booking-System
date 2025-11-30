"""
School Activity Booking System - Flask Application
Main application entry point
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, abort, make_response
# Trigger reload
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from flask import send_file
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from config import config

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    
    # Register context processors
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
        


    return app

app = create_app()

# ==================== Database Models ====================

class Parent(db.Model):
    """Parent/Guardian model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='parent', lazy=True, cascade='all, delete-orphan')
    children = db.relationship('Child', backref='parent', lazy=True, cascade='all, delete-orphan')
    waitlists = db.relationship('Waitlist', backref='parent', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Admin(db.Model):
    """Admin model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Tutor(db.Model):
    """Tutor model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(100))
    bio = db.Column(db.Text)
    qualifications = db.Column(db.Text)  # Educational background
    photo_url = db.Column(db.String(200), default='default-avatar.png')  # Profile photo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    activities = db.relationship('Activity', backref='tutor', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Child(db.Model):
    """Child model"""
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    grade = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='child', lazy=True, cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', backref='child', lazy=True, cascade='all, delete-orphan')

class Activity(db.Model):
    """Available activities model"""
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    max_capacity = db.Column(db.Integer, default=20)
    day_of_week = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='activity', lazy=True, cascade='all, delete-orphan')
    waitlists = db.relationship('Waitlist', backref='activity', lazy=True, cascade='all, delete-orphan')

class Booking(db.Model):
    """Booking model"""
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='confirmed') # confirmed, cancelled
    cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('child_id', 'booking_date', name='unique_booking_per_day'),)

class Waitlist(db.Model):
    """Waitlist model"""
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='waiting') # waiting, notified, expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    """Attendance model"""
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='present') # present, absent, late
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemLog(db.Model):
    """Audit log for security"""
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20)) # admin, tutor, parent
    user_id = db.Column(db.Integer)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ==================== Helpers & Decorators ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'parent_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def tutor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'tutor_id' not in session:
            return redirect(url_for('tutor_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def promote_waitlist_user(activity_id, booking_date):
    """
    Promotes the oldest waitlisted user for a specific activity and date.
    """
    # Find oldest waitlist entry
    next_in_line = Waitlist.query.filter_by(
        activity_id=activity_id,
        request_date=booking_date,
        status='waiting'
    ).order_by(Waitlist.created_at.asc()).first()
    
    if next_in_line:
        # Create booking for them
        activity = Activity.query.get(activity_id)
        new_booking = Booking(
            parent_id=next_in_line.parent_id,
            child_id=next_in_line.child_id,
            activity_id=activity_id,
            booking_date=booking_date,
            cost=activity.price,
            status='confirmed'
        )
        
        # Update waitlist status
        next_in_line.status = 'promoted'
        
        db.session.add(new_booking)
        db.session.commit()
        
        # In a real app, we would send an email here
        print(f"Promoted child {next_in_line.child_id} from waitlist for activity {activity_id}")
        return True
    return False

# Helper function to generate .ics calendar file
def generate_ics_file(booking):
    """Generate iCalendar (.ics) file for booking"""
    activity = booking.activity
    child = booking.child
    
    # Parse time strings
    start_time_str = activity.start_time
    end_time_str = activity.end_time
    
    # Create datetime objects for the event
    event_date = booking.booking_date
    start_hour, start_min = map(int, start_time_str.split(':'))
    end_hour, end_min = map(int, end_time_str.split(':'))
    
    start_datetime = datetime.combine(event_date, datetime.min.time()).replace(hour=start_hour, minute=start_min)
    end_datetime = datetime.combine(event_date, datetime.min.time()).replace(hour=end_hour, minute=end_min)
    
    # Format for iCal (YYYYMMDDTHHmmss)
    dtstart = start_datetime.strftime('%Y%m%dT%H%M%S')
    dtend = end_datetime.strftime('%Y%m%dT%H%M%S')
    dtstamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    
    tutor_name = activity.tutor.full_name if activity.tutor else 'To Be Assigned'
    
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Greenwood International School//Activity Booking//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
DTSTART:{dtstart}
DTEND:{dtend}
DTSTAMP:{dtstamp}
UID:booking-{booking.id}@greenwood.edu.uk
SUMMARY:{activity.name} - {child.name}
DESCRIPTION:Activity: {activity.name}\\nStudent: {child.name}\\nTutor: {tutor_name}\\nDay: {activity.day_of_week}\\nTime: {start_time_str} - {end_time_str}\\n\\n{activity.description}
LOCATION:Greenwood International School\\, Henley-on-Thames
ORGANIZER;CN={tutor_name}:mailto:info@greenwood.edu.uk
STATUS:CONFIRMED
SEQUENCE:0
BEGIN:VALARM
TRIGGER:-PT24H
ACTION:DISPLAY
DESCRIPTION:Reminder: {activity.name} tomorrow
END:VALARM
END:VEVENT
END:VCALENDAR"""
    
    return ics_content

# Helper function to send booking confirmation emails
def send_booking_confirmation_email(booking):
    """Send booking confirmation email to parent and tutor with .ics attachment"""
    try:
        parent = booking.parent
        child = booking.child
        activity = booking.activity
        tutor = activity.tutor
        
        # Generate .ics calendar file
        ics_content = generate_ics_file(booking)
        
        # === Email to Parent ===
        parent_msg = Message(
            subject=f'Booking Confirmed: {activity.name} for {child.name}',
            sender=('Greenwood International School', 'noreply@greenwood.edu.uk'),
            recipients=[parent.email]
        )
        
        parent_msg.html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #002E5D; border-bottom: 3px solid #0DA49F; padding-bottom: 10px;">
                    Booking Confirmation
                </h2>
                
                <p>Dear {parent.full_name},</p>
                
                <p>Thank you for booking an activity at Greenwood International School. Your booking has been confirmed!</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #002E5D; margin-top: 0;">Booking Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold; width: 40%;">Booking ID:</td>
                            <td style="padding: 8px 0;">#{booking.id}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Activity:</td>
                            <td style="padding: 8px 0;">{activity.name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Student:</td>
                            <td style="padding: 8px 0;">{child.name} (Year {child.grade})</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Date:</td>
                            <td style="padding: 8px 0;">{booking.booking_date.strftime('%A, %d %B %Y')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Time:</td>
                            <td style="padding: 8px 0;">{activity.start_time} - {activity.end_time}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Day:</td>
                            <td style="padding: 8px 0;">{activity.day_of_week}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Tutor:</td>
                            <td style="padding: 8px 0;">{tutor.full_name if tutor else 'To Be Assigned'}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Amount Paid:</td>
                            <td style="padding: 8px 0; color: #28a745; font-weight: bold;">£{booking.cost:.2f}</td>
                        </tr>
                    </table>
                </div>
                
                <p><strong>📅 Calendar Invite:</strong> A calendar invitation (.ics file) is attached to this email. Click to add this event to your calendar!</p>
                
                <p style="margin-top: 30px;">If you have any questions, please don't hesitate to contact us.</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                    <p><strong>Greenwood International School</strong><br>
                    Greenwood Hall, Henley-on-Thames, Oxfordshire, RG9 1AA<br>
                    📧 greenwoodinternationaluk@gmail.com | 📞 +44 20 7123 4567</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach .ics file to parent email
        parent_msg.attach(
            filename=f'booking_{booking.id}.ics',
            content_type='text/calendar',
            data=ics_content
        )
        
        # === Email to Tutor ===
        if tutor and tutor.email:
            tutor_msg = Message(
                subject=f'New Student Enrolled: {activity.name}',
                sender=('Greenwood International School', 'noreply@greenwood.edu.uk'),
                recipients=[tutor.email]
            )
            
            tutor_msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #002E5D;">New Student Enrollment</h2>
                    
                    <p>Dear {tutor.full_name},</p>
                    
                    <p>A new student has been enrolled in your activity:</p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="color: #002E5D; margin-top: 0;">Enrollment Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold; width: 40%;">Activity:</td>
                                <td style="padding: 8px 0;">{activity.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold;">Student:</td>
                                <td style="padding: 8px 0;">{child.name} (Year {child.grade}, Age {child.age})</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold;">Parent:</td>
                                <td style="padding: 8px 0;">{parent.full_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold;">Date:</td>
                                <td style="padding: 8px 0;">{booking.booking_date.strftime('%A, %d %B %Y')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold;">Schedule:</td>
                                <td style="padding: 8px 0;">{activity.day_of_week}, {activity.start_time} - {activity.end_time}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p>📅 A calendar invitation is attached. Please add this session to your calendar.</p>
                    
                    <p>Please prepare materials and ensure the session venue is ready.</p>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                        <p><strong>Greenwood International School</strong><br>
                        📧 greenwoodinternationaluk@gmail.com | 📞 +44 20 7123 4567</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Attach .ics file to tutor email
            tutor_msg.attach(
                filename=f'{activity.name}_{child.name}.ics',
                content_type='text/calendar',
                data=ics_content
            )
            
            mail.send(tutor_msg)
        
        # Send parent email
        mail.send(parent_msg)
        
        return True
        
    except Exception as e:
        print(f'❌ Email sending failed: {str(e)}')
        # Don't fail the booking if email fails
        return False

# ==================== Routes ====================

@app.route('/')
def index():
    """School Home Page"""
    return render_template('school/home.html')

@app.route('/portal')
def portal_home():
    """Portal Entry Point"""
    return render_template('index.html')

@app.route('/admissions')
def admissions():
    """Admissions Page"""
    return render_template('school/admissions.html')

@app.route('/academic')
def academic():
    """Academic Page"""
    return render_template('school/academic.html')

@app.route('/alumni')
def alumni():
    """Alumni Page"""
    return render_template('school/alumni.html')

# --- Authentication ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        
        # Validation
        if not all([email, password, confirm_password, full_name, phone]):
            return render_template('register.html', error='All fields are required')
        
        # Email Validation
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return render_template('register.html', error='Invalid email address format')

        # Phone Validation (Digits, +, -, space)
        phone_regex = r'^[0-9+\s-]{10,15}$'
        if not re.match(phone_regex, phone):
            return render_template('register.html', error='Invalid phone number. Use 10-15 digits.')

        # Password Strength
        if len(password) < 8:
            return render_template('register.html', error='Password must be at least 8 characters long')

        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        if Parent.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already registered')
        
        parent = Parent(email=email, full_name=full_name, phone=phone)
        parent.set_password(password)
        db.session.add(parent)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        parent = Parent.query.filter_by(email=email).first()
        
        if parent and parent.check_password(password):
            session['parent_id'] = parent.id
            session['parent_name'] = parent.full_name
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('portal_home'))

# --- Parent Dashboard ---

@app.route('/dashboard')
@login_required
def dashboard():
    
    parent = Parent.query.get(session['parent_id'])
    bookings = Booking.query.filter_by(parent_id=session['parent_id'], status='confirmed').all()
    children = parent.children
    activities = Activity.query.all()
    
    return render_template('dashboard.html', parent=parent, bookings=bookings, children=children, activities=activities)

@app.route('/add_child', methods=['POST'])
@login_required
def add_child():
    
    name = request.form.get('name')
    age = request.form.get('age')
    grade = request.form.get('grade')
    
    if not name:
        return jsonify({'error': 'Child name is required'}), 400
    
    child = Child(parent_id=session['parent_id'], name=name, age=age, grade=grade)
    db.session.add(child)
    db.session.commit()
    
    return jsonify({'id': child.id, 'name': child.name})

@app.route('/remove_child/<int:child_id>', methods=['POST'])
@login_required
def remove_child(child_id):
    
    child = Child.query.get_or_404(child_id)
    if child.parent_id != session['parent_id']:
        return jsonify({'error': 'Unauthorized'}), 403
        
    db.session.delete(child)
    db.session.commit()
    return jsonify({'success': True})

# --- API Routes ---

@app.route('/api/activities')
def api_activities():
    activities = Activity.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'price': a.price,
        'day': a.day_of_week,
        'time': f"{a.start_time} - {a.end_time}",
        'capacity': a.max_capacity
    } for a in activities])

@app.route('/api/check_availability', methods=['POST'])
def check_availability():
    data = request.get_json()
    activity_id = data.get('activity_id')
    date_str = data.get('booking_date')
    
    try:
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return jsonify({'error': 'Invalid date'}), 400
        
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
        
    count = Booking.query.filter_by(
        activity_id=activity_id, 
        booking_date=booking_date, 
        status='confirmed'
    ).count()
    
    return jsonify({
        'available': count < activity.max_capacity,
        'spots_left': activity.max_capacity - count
    })

@app.route('/payment/<int:activity_id>/<int:child_id>/<date>')
@login_required
def payment_page(activity_id, child_id, date):
    activity = Activity.query.get_or_404(activity_id)
    child = Child.query.get_or_404(child_id)
    
    if child.parent_id != session['parent_id']:
        return redirect(url_for('dashboard'))
        
    return render_template('payment.html', activity=activity, child=child, date=date)

@app.route('/book_activity', methods=['POST'])
@login_required
def book_activity():
    
    child_id = request.form.get('child_id')
    activity_id = request.form.get('activity_id')
    booking_date_str = request.form.get('booking_date')
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    try:
        booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        msg = 'Invalid date format'
        if is_ajax:
            return jsonify({'error': msg}), 400
        flash(msg, 'danger')
        return redirect(url_for('dashboard'))
    
    child = Child.query.get(child_id)
    activity = Activity.query.get(activity_id)
    
    if not child or not activity:
        msg = 'Invalid child or activity'
        if is_ajax:
            return jsonify({'error': msg}), 400
        flash(msg, 'danger')
        return redirect(url_for('dashboard'))
    
    if child.parent_id != session['parent_id']:
        msg = 'Unauthorized'
        if is_ajax:
            return jsonify({'error': msg}), 403
        flash(msg, 'danger')
        return redirect(url_for('dashboard'))
    
    # Check conflict
    existing_booking = Booking.query.filter_by(
        child_id=child_id,
        booking_date=booking_date,
        status='confirmed'
    ).first()
    
    if existing_booking:
        msg = f'Child already has a booking on {booking_date}'
        if is_ajax:
            return jsonify({'error': msg}), 400
        flash(msg, 'warning')
        return redirect(url_for('dashboard'))
    
    # Check capacity
    bookings_count = Booking.query.filter_by(activity_id=activity_id, booking_date=booking_date, status='confirmed').count()
    if bookings_count >= activity.max_capacity:
        # Offer Waitlist
        msg = 'Activity is full'
        if is_ajax:
            return jsonify({'error': msg, 'full': True}), 400
        flash(msg, 'warning')
        return redirect(url_for('dashboard'))
    
    # Create booking
    booking = Booking(
        parent_id=session['parent_id'],
        child_id=child_id,
        activity_id=activity_id,
        booking_date=booking_date,
        cost=activity.price
    )
    db.session.add(booking)
    db.session.commit()
    
    # Send confirmation emails (non-blocking)
    try:
        send_booking_confirmation_email(booking)
        print(f'✅ Confirmation emails sent for booking #{booking.id}')
    except Exception as e:
        print(f'⚠️ Email sending skipped: {str(e)}')
    
    if is_ajax:
        return jsonify({'success': True, 'message': 'Booking confirmed!', 'booking_id': booking.id})
    
    flash('Booking confirmed successfully!', 'success')
    return redirect(url_for('booking_success', booking_id=booking.id))

@app.route('/booking_success/<int:booking_id>')
@login_required
def booking_success(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.parent_id != session['parent_id']:
        return redirect(url_for('dashboard'))
    return render_template('booking_success.html', booking=booking)

@app.route('/join_waitlist', methods=['POST'])
@login_required
def join_waitlist():
        
    child_id = request.form.get('child_id')
    activity_id = request.form.get('activity_id')
    date_str = request.form.get('date')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return jsonify({'error': 'Invalid date'}), 400
        
    waitlist = Waitlist(
        parent_id=session['parent_id'],
        child_id=child_id,
        activity_id=activity_id,
        request_date=date
    )
    db.session.add(waitlist)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Added to waitlist'})

@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if not booking or booking.parent_id != session['parent_id']:
        msg = 'Unauthorized'
        if is_ajax:
            return jsonify({'error': msg}), 403
        flash(msg, 'danger')
        return redirect(url_for('dashboard'))
    
    # Store details for waitlist check before deleting/cancelling
    activity_id = booking.activity_id
    booking_date = booking.booking_date
    
    booking.status = 'cancelled'
    db.session.commit()
    
    # Check waitlist and promote if applicable
    promoted = promote_waitlist_user(activity_id, booking_date)
    message = 'Booking cancelled.'
    if promoted:
        message += ' A spot opened up and was filled from the waitlist.'
    
    if is_ajax:
        return jsonify({'success': True, 'message': message})
    
    flash(message, 'info')
    return redirect(url_for('dashboard'))

@app.route('/invoice/<int:booking_id>')
@login_required
def generate_invoice(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.parent_id != session['parent_id']:
        abort(403)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=10,
        alignment=1  # Center
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=5,
        alignment=1
    )
    
    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=1
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=8,
        spaceBefore=15
    )
    
    # Header Section
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Paragraph("Greenwood International School", subtitle_style))
    elements.append(Paragraph("123 Education Lane, London, UK SW1A 1AA", small_style))
    elements.append(Paragraph("Tel: +44 (0) 1491 570000 | Email: greenwoodinternationaluk@gmail.com", small_style))
    elements.append(Paragraph("Company Registration No: 12345678 | VAT No: GB123456789", small_style))
    elements.append(Spacer(1, 25))
    
    # Invoice Info and Client Info Side by Side
    invoice_info = [
        ["Invoice Number:", f"INV-{booking.id:06d}"],
        ["Invoice Date:", datetime.now().strftime('%d %B %Y')],
        ["Booking Date:", booking.booking_date.strftime('%d %B %Y')],
        ["Payment Status:", "PAID"],
        ["Payment Method:", "Online Payment"]
    ]
    
    client_info = [
        ["Bill To:", ""],
        ["", booking.parent.full_name],
        ["", booking.parent.email],
        ["Student:", booking.child.name],
        ["Year Group:", f"Grade {booking.child.grade}"]
    ]
    
    # Create two-column layout for invoice and client info
    info_table_data = []
    for i in range(max(len(invoice_info), len(client_info))):
        row = []
        if i < len(invoice_info):
            row.extend(invoice_info[i])
        else:
            row.extend(["", ""])
        row.append("")  # Spacer column
        if i < len(client_info):
            row.extend(client_info[i])
        else:
            row.extend(["", ""])
        info_table_data.append(row)
    
    info_table = Table(info_table_data, colWidths=[90, 150, 20, 80, 140])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
        ('TEXTCOLOR', (3, 0), (3, -1), colors.HexColor('#555555')),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    
    # Activity Details Section
    elements.append(Paragraph("Activity Details", section_heading))
    
    activity_details = [
        ["Activity Name:", booking.activity.name],
        ["Day of Week:", booking.activity.day_of_week],
        ["Time:", f"{booking.activity.start_time} - {booking.activity.end_time}"],
        ["Tutor:", booking.activity.tutor.full_name if booking.activity.tutor else "To Be Assigned"],
        ["Description:", booking.activity.description[:100] + "..." if len(booking.activity.description) > 100 else booking.activity.description]
    ]
    
    activity_table = Table(activity_details, colWidths=[120, 360])
    activity_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
    ]))
    elements.append(activity_table)
    elements.append(Spacer(1, 20))
    
    # Line Items Section
    elements.append(Paragraph("Charges", section_heading))
    
    items = [
        ["Description", "Scheduled Date", "Unit Price", "Quantity", "Amount"],
        [
            booking.activity.name,
            booking.booking_date.strftime('%d %b %Y'),
            f"£{booking.cost:.2f}",
            "1",
            f"£{booking.cost:.2f}"
        ]
    ]
    
    # Add subtotal and total rows
    items.append(["", "", "", "Subtotal:", f"£{booking.cost:.2f}"])
    items.append(["", "", "", "VAT (0%):", "£0.00"])
    items.append(["", "", "", "Total:", f"£{booking.cost:.2f}"])
    
    table = Table(items, colWidths=[180, 100, 80, 80, 80])
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Data row
        ('ALIGN', (0, 1), (0, 1), 'LEFT'),
        ('ALIGN', (1, 1), (-1, 1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, 1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
        ('TOPPADDING', (0, 1), (-1, 1), 8),
        ('GRID', (0, 0), (-1, 1), 0.5, colors.grey),
        
        # Subtotal, VAT, Total rows
        ('ALIGN', (3, 2), (-1, -1), 'RIGHT'),
        ('FONTNAME', (3, 2), (3, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 2), (-1, -1), 10),
        ('LINEABOVE', (3, 2), (-1, 2), 0.5, colors.grey),
        ('LINEABOVE', (3, -1), (-1, -1), 1.5, colors.HexColor('#0d6efd')),
        ('FONTNAME', (3, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (3, -1), (-1, -1), 12),
        ('TEXTCOLOR', (3, -1), (-1, -1), colors.HexColor('#0d6efd')),
        ('BOTTOMPADDING', (0, 2), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 30))
    
    # Payment Information
    elements.append(Paragraph("Payment Information", section_heading))
    payment_info = Paragraph(
        "Payment has been received in full for this booking. This invoice serves as a receipt for your records.",
        styles['Normal']
    )
    elements.append(payment_info)
    elements.append(Spacer(1, 20))
    
    # Terms and Conditions
    elements.append(Paragraph("Terms & Conditions", section_heading))
    terms = [
        "1. Cancellations must be made at least 48 hours in advance for a full refund.",
        "2. Late arrivals may result in reduced session time without refund.",
        "3. Parents/guardians are responsible for ensuring children are collected on time.",
        "4. The school reserves the right to cancel activities due to unforeseen circumstances.",
        "5. All personal information is handled in accordance with GDPR regulations."
    ]
    
    for term in terms:
        elements.append(Paragraph(term, ParagraphStyle('Terms', parent=styles['Normal'], fontSize=8, leftIndent=10)))
    
    elements.append(Spacer(1, 30))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#0d6efd'),
        alignment=1
    )
    elements.append(Paragraph("Thank you for choosing Greenwood International School!", footer_style))
    elements.append(Paragraph("For any queries, please contact us at greenwoodinternationaluk@gmail.com or +44 (0) 1491 570000", small_style))
    
    doc.build(elements)
    buffer.seek(0)
    
    # Create response with proper headers for PDF download
    # Using inline with proper filename encoding to ensure correct filename in all browsers
    invoice_filename = f'Invoice_{booking.id:06d}_Greenwood.pdf'
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="{invoice_filename}"'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

# --- Admin Routes ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/login.html', error='Invalid credentials')
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(db.func.sum(Booking.cost)).scalar() or 0
    activities = Activity.query.all()
    tutors = Tutor.query.all()
    
    return render_template('admin/dashboard.html', 
                           total_bookings=total_bookings, 
                           total_revenue=total_revenue,
                           activities=activities,
                           tutors=tutors)

@app.route('/admin/activity/add', methods=['POST'])
@admin_required
def add_activity():
        
    # Logic to add activity
    name = request.form.get('name')
    try:
        price = float(request.form.get('price'))
    except (ValueError, TypeError):
        flash('Invalid price format', 'error')
        return redirect(url_for('admin_dashboard'))
        
    day = request.form.get('day')
    start = request.form.get('start')
    end = request.form.get('end')
    tutor_id = request.form.get('tutor_id')
    
    activity = Activity(name=name, price=price, day_of_week=day, start_time=start, end_time=end)
    if tutor_id:
        activity.tutor_id = tutor_id
        
    db.session.add(activity)
    db.session.commit()
    
    flash('Activity created successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/tutor/add', methods=['POST'])
@admin_required
def add_tutor():
        
    email = request.form.get('email')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    specialization = request.form.get('specialization')
    
    if Tutor.query.filter_by(email=email).first():
        flash('Email already registered', 'error')
        return redirect(url_for('admin_dashboard'))
        
    tutor = Tutor(email=email, full_name=full_name, specialization=specialization)
    tutor.set_password(password)
    db.session.add(tutor)
    db.session.commit()
    
    flash('Tutor added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/tutor/delete/<int:id>', methods=['POST'])
@admin_required
def delete_tutor(id):
    tutor = Tutor.query.get_or_404(id)
    
    # Unassign from activities first
    for activity in tutor.activities:
        activity.tutor_id = None
        
    db.session.delete(tutor)
    db.session.commit()
    flash('Tutor deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/activity/delete/<int:id>', methods=['POST'])
@admin_required
def delete_activity(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    flash('Activity deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/tutor/edit/<int:id>', methods=['POST'])
@admin_required
def edit_tutor(id):
    tutor = Tutor.query.get_or_404(id)
    
    tutor.full_name = request.form.get('full_name')
    tutor.email = request.form.get('email')
    tutor.specialization = request.form.get('specialization')
    
    if request.form.get('password'):
        tutor.set_password(request.form.get('password'))
        
    db.session.commit()
    flash('Tutor updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/activity/edit/<int:id>', methods=['POST'])
@admin_required
def edit_activity(id):
    activity = Activity.query.get_or_404(id)
    
    activity.name = request.form.get('name')
    try:
        activity.price = float(request.form.get('price'))
    except (ValueError, TypeError):
        flash('Invalid price format', 'error')
        return redirect(url_for('admin_dashboard'))
        
    activity.day_of_week = request.form.get('day')
    activity.start_time = request.form.get('start')
    activity.end_time = request.form.get('end')
    
    tutor_id = request.form.get('tutor_id')
    if tutor_id:
        activity.tutor_id = tutor_id
    else:
        activity.tutor_id = None
        
    db.session.commit()
    flash('Activity updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# --- Tutor Routes ---

@app.route('/tutor/login', methods=['GET', 'POST'])
def tutor_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        tutor = Tutor.query.filter_by(email=email).first()
        if tutor and tutor.check_password(password):
            session['tutor_id'] = tutor.id
            session['tutor_name'] = tutor.full_name
            return redirect(url_for('tutor_dashboard'))
        return render_template('tutor/login.html', error='Invalid credentials')
    return render_template('tutor/login.html')

@app.route('/tutor/dashboard')
@tutor_required
def tutor_dashboard():
    
    tutor = Tutor.query.get(session['tutor_id'])
    # Get activities assigned to this tutor
    activities = Activity.query.filter_by(tutor_id=tutor.id).all()
    
    return render_template('tutor/dashboard.html', tutor=tutor, activities=activities)

@app.route('/tutor/attendance/<int:activity_id>', methods=['GET', 'POST'])
@tutor_required
def tutor_attendance(activity_id):
    
    activity = Activity.query.get_or_404(activity_id)
    if activity.tutor_id != session['tutor_id']:
        return redirect(url_for('tutor_dashboard'))
        
    if request.method == 'POST':
        date_str = request.form.get('date')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            date = datetime.utcnow().date()
            
        # Process attendance for each student
        bookings = Booking.query.filter_by(activity_id=activity_id, status='confirmed').all()
        for booking in bookings:
            status = request.form.get(f'status_{booking.child.id}')
            notes = request.form.get(f'notes_{booking.child.id}')
            
            # Check if record exists
            record = Attendance.query.filter_by(
                child_id=booking.child.id,
                activity_id=activity_id,
                date=date
            ).first()
            
            if record:
                record.status = status
            else:
                record = Attendance(
                    child_id=booking.child.id,
                    activity_id=activity_id,
                    date=date,
                    status=status
                )
                db.session.add(record)
        
        db.session.commit()
        flash('Attendance recorded successfully!', 'success')
        return redirect(url_for('tutor_dashboard'))
    
    # GET request - show attendance form
    bookings = Booking.query.filter_by(activity_id=activity_id, status='confirmed').all()
    return render_template('tutor/attendance.html', 
                         activity=activity, 
                         bookings=bookings,
                         today=datetime.utcnow().date())

@app.route('/tutor/attendance_history/<int:activity_id>')
@tutor_required
def attendance_history(activity_id):
    """View attendance history for an activity"""
    tutor_id = session['tutor_id']
    
    activity = Activity.query.get_or_404(activity_id)
    if activity.tutor_id != tutor_id:
        return redirect(url_for('tutor_dashboard'))
    
    # Get all attendance records for this activity, grouped by date
    from sqlalchemy import func
    from sqlalchemy.sql import case
    
    attendance_records = db.session.query(
        Attendance.date,
        func.count(Attendance.id).label('total'),
        func.sum(case((Attendance.status == 'present', 1), else_=0)).label('present'),
        func.sum(case((Attendance.status == 'late', 1), else_=0)).label('late'),
        func.sum(case((Attendance.status == 'absent', 1), else_=0)).label('absent')
    ).filter_by(activity_id=activity_id).group_by(Attendance.date).order_by(Attendance.date.desc()).all()
    
    # Get detailed records for each date
    detailed_records = {}
    for record in attendance_records:
        date = record.date
        detailed_records[date] = Attendance.query.filter_by(
            activity_id=activity_id,
            date=date
        ).join(Child).all()
    
    return render_template('tutor/attendance_history.html',
                         activity=activity,
                         attendance_records=attendance_records,
                         detailed_records=detailed_records)

# --- DB Init ---

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create Default Admin
        if not Admin.query.filter_by(email='admin@school.edu').first():
            admin = Admin(email='admin@school.edu')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin created: admin@school.edu / admin123")
            
        # Create Sample Tutor
        if not Tutor.query.filter_by(email='tutor@school.edu').first():
            tutor = Tutor(email='tutor@school.edu', full_name='Sarah Jenkins', specialization='Science & Robotics')
            tutor.set_password('tutor123')
            db.session.add(tutor)
            db.session.commit()
            print("Tutor created: tutor@school.edu / tutor123")
            
        # Create Sample Activities (Assigned to Tutor)
        if Activity.query.count() == 0:
            tutor = Tutor.query.filter_by(email='tutor@school.edu').first()
            activities = [
                Activity(name='Robotics Club', description='Build robots', price=50.0, day_of_week='Monday', start_time='15:00', end_time='16:30', tutor_id=tutor.id),
                Activity(name='Swimming', description='Pool time', price=30.0, day_of_week='Tuesday', start_time='15:00', end_time='16:30', tutor_id=tutor.id),
            ]
            db.session.add_all(activities)
            db.session.commit()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
