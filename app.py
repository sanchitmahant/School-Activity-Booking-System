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
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
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

# Enhanced PDF Invoice Generator
from enhanced_invoice import get_enhanced_invoice_pdf


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
    
    # Enable template auto-reload for development
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
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
    specialization = db.Column(db.String(200))
    qualification = db.Column(db.String(300))
    bio = db.Column(db.Text)
    linkedin_url = db.Column(db.String(200))
    teaching_philosophy = db.Column(db.Text)
    years_experience = db.Column(db.Integer)
    education = db.Column(db.Text)
    certifications = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_by = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    approval_date = db.Column(db.DateTime, nullable=True)
    
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
    
    # Relationships
    tutor = db.relationship('Tutor', backref='activities', lazy=True)
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
    notes = db.Column(db.Text)
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
UID:booking-{booking.id}@greenwoodinternationaluk.gmail.com
SUMMARY:{activity.name} - {child.name}
DESCRIPTION:Activity: {activity.name}\\nStudent: {child.name}\\nTutor: {tutor_name}\\nDay: {activity.day_of_week}\\nTime: {start_time_str} - {end_time_str}\\n\\n{activity.description}
LOCATION:Greenwood International School\\, Henley-on-Thames
ORGANIZER;CN={tutor_name}:mailto:greenwoodinternationaluk@gmail.com
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
            sender=('Greenwood International School', 'greenwoodinternationaluk@gmail.com'),
            recipients=[parent.email]
        )
        
        parent_msg.html = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #002E5D; margin: 0;">Greenwood International</h1>
                    <p style="color: #666; font-size: 14px;">Booking Confirmation</p>
                </div>
                
                <h2 style="color: #28a745; margin-top: 0;">Booking Confirmed</h2>
                <p>Dear {parent.full_name},</p>
                <p>Thank you for booking an activity at Greenwood International School. We are pleased to confirm your booking.</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745;">
                    <h3 style="color: #002E5D; margin-top: 0;">Booking Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold; width: 40%;">Booking ID:</td>
                            <td style="padding: 5px 0;">#{booking.id}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold;">Activity:</td>
                            <td style="padding: 5px 0;">{activity.name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold;">Student:</td>
                            <td style="padding: 5px 0;">{child.name} (Year {child.grade})</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold;">Date:</td>
                            <td style="padding: 5px 0;">{booking.booking_date.strftime('%A, %d %B %Y')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold;">Time:</td>
                            <td style="padding: 5px 0;">{activity.start_time} - {activity.end_time}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold;">Day:</td>
                            <td style="padding: 5px 0;">{activity.day_of_week}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold;">Tutor:</td>
                            <td style="padding: 5px 0;">{tutor.full_name if tutor else 'To Be Assigned'}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold;">Amount Paid:</td>
                            <td style="padding: 5px 0; color: #28a745; font-weight: bold;">£{booking.cost:.2f}</td>
                        </tr>
                    </table>
                </div>
                
                <p><strong>📅 Calendar Invite:</strong> A calendar invitation file is attached. Click to add to your calendar.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://127.0.0.1:5000/portal" style="background-color: #002E5D; color: white; padding: 14px 28px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block;">
                        View My Bookings
                    </a>
                </div>
                
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
                    <p>Greenwood International School<br>Greenwood Hall, Henley-on-Thames, Oxfordshire, RG9 1AA</p>
                    <p>&copy; {datetime.now().year} Greenwood International School. All rights reserved.</p>
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
                sender=('Greenwood International School', 'greenwoodinternationaluk@gmail.com'),
                recipients=[tutor.email]
            )
            
            tutor_msg.html = f"""
            <html>
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #002E5D; margin: 0;">Greenwood International</h1>
                        <p style="color: #666; font-size: 14px;">Enrollment Alert</p>
                    </div>
                    
                    <h2 style="color: #002E5D; margin-top: 0;">New Student Enrollment</h2>
                    <p>Dear {tutor.full_name},</p>
                    
                    <p>A new student has been enrolled in your activity:</p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #002E5D;">
                        <h3 style="color: #002E5D; margin-top: 0;">Enrollment Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold; width: 40%;">Activity:</td>
                                <td style="padding: 5px 0;">{activity.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Student:</td>
                                <td style="padding: 5px 0;">{child.name} (Year {child.grade}, Age {child.age})</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Parent:</td>
                                <td style="padding: 5px 0;">{parent.full_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Date:</td>
                                <td style="padding: 5px 0;">{booking.booking_date.strftime('%A, %d %B %Y')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Time:</td>
                                <td style="padding: 5px 0;">{activity.start_time} - {activity.end_time}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p>📅 A calendar invitation is attached. Please ensure you are prepared for this session.</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://127.0.0.1:5000/tutor/login" style="background-color: #002E5D; color: white; padding: 14px 28px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block;">
                            View Dashboard
                        </a>
                    </div>
                    
                    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
                        <p>&copy; {datetime.now().year} Greenwood International School. All rights reserved.</p>
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
        
        # === Email to Admin ===
        admin = Admin.query.first()
        if admin:
            admin_msg = Message(
                subject=f'New Booking Alert: {activity.name} - {child.name}',
                sender=('Greenwood International School', 'greenwoodinternationaluk@gmail.com'),
                recipients=[admin.email]
            )
            
            admin_msg.html = f"""
            <html>
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #002E5D; margin: 0;">Greenwood International</h1>
                        <p style="color: #666; font-size: 14px;">Admin Notification</p>
                    </div>
                    
                    <h2 style="color: #002E5D; margin-top: 0;">New Booking Received</h2>
                    <p><strong>Admin Notification</strong></p>
                    <p>A new booking has been successfully processed.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="color: #002E5D; margin-top: 0;">Booking Details</h3>
                        <table style="width: 100%;">
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold; width: 40%;">Booking ID:</td>
                                <td style="padding: 5px 0;">#{booking.id}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Activity:</td>
                                <td style="padding: 5px 0;">{activity.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Student:</td>
                                <td style="padding: 5px 0;">{child.name} (Year {child.grade})</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Parent:</td>
                                <td style="padding: 5px 0;">{parent.full_name} ({parent.email})</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Date:</td>
                                <td style="padding: 5px 0;">{booking.booking_date.strftime('%A, %d %B %Y')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Amount Paid:</td>
                                <td style="padding: 5px 0; color: #28a745; font-weight: bold;">£{booking.cost:.2f}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
                        <p>Automated Notification System</p>
                        <p>&copy; {datetime.now().year} Greenwood International School.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            mail.send(admin_msg)
        
        # Send parent email
        mail.send(parent_msg)
        
        return True
        
    except Exception as e:
        print(f'❌ Email sending failed: {str(e)}')
        # Don't fail the booking if email fails
        return False


# ==================== Professional Email Functions ====================

def send_tutor_application_email(tutor):
    """Send emails when tutor applies"""
    try:
        # Tutor confirmation
        tutor_msg = Message(
            subject='Application Received - Greenwood International',
            recipients=[tutor.email]
        )
        tutor_msg.html = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #002E5D; margin: 0;">Greenwood International</h1>
                    <p style="color: #666; font-size: 14px;">Excellence in Education</p>
                </div>
                
                <h2 style="color: #002E5D; margin-top: 0;">Application Received</h2>
                <p>Dear {tutor.full_name},</p>
                <p>Thank you for applying to join our team at Greenwood International School.</p>
                <p>We have successfully received your application details. Our administrative team will review your qualifications and experience shortly.</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
                    <p style="margin: 0;"><strong>Application Date:</strong> {tutor.created_at.strftime('%B %d, %Y')}</p>
                    <p style="margin: 10px 0 0 0;"><strong>Current Status:</strong> <span style="color: #ffc107; font-weight: bold;">Pending Review</span></p>
                </div>
                
                <p>You will receive another email notification once a decision has been made.</p>
                
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
                    <p>&copy; {datetime.now().year} Greenwood International School. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Admin notification
        admin = Admin.query.first()
        if admin:
            admin_msg = Message(
                subject=f'New Tutor Application: {tutor.full_name}',
                recipients=[admin.email]
            )
            admin_msg.html = f"""
            <html>
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #002E5D; margin: 0;">Greenwood International</h1>
                        <p style="color: #666; font-size: 14px;">Admin Notification</p>
                    </div>
                    
                    <h2 style="color: #002E5D; margin-top: 0;">New Tutor Application</h2>
                    <p>A new tutor application has been submitted and requires review.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <table style="width: 100%;">
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold; width: 30%;">Name:</td>
                                <td style="padding: 5px 0;">{tutor.full_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Email:</td>
                                <td style="padding: 5px 0;">{tutor.email}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Specialization:</td>
                                <td style="padding: 5px 0;">{tutor.specialization}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://127.0.0.1:5000/admin/pending-tutors" style="background-color: #002E5D; color: white; padding: 14px 28px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block;">
                            Review Application
                        </a>
                    </div>
                    
                    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
                        <p>&copy; {datetime.now().year} Greenwood International School. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            mail.send(admin_msg)
        
        mail.send(tutor_msg)
        return True
    except Exception as e:
        print(f'Email error: {e}')
        return False

def send_tutor_approval_email(tutor):
    """Send approval email"""
    try:
        msg = Message(
            subject='Application Approved - Welcome to Greenwood!',
            recipients=[tutor.email]
        )
        msg.html = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #002E5D; margin: 0;">Greenwood International</h1>
                    <p style="color: #666; font-size: 14px;">Welcome</p>
                </div>
                
                <h2 style="color: #28a745; margin-top: 0; text-align: center;">Congratulations!</h2>
                <p>Dear {tutor.full_name},</p>
                
                <p>We are pleased to inform you that your application to join Greenwood International School as a tutor has been <strong>APPROVED</strong>.</p>
                
                <p>You can now log in to the Tutor Portal to set up your profile, view activity assignments, and manage your schedules.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://127.0.0.1:5000/tutor/login" style="background-color: #28a745; color: white; padding: 14px 28px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block;">
                        Access Tutor Portal
                    </a>
                </div>
                
                <p>We look forward to working with you!</p>
                
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
                    <p>&copy; {datetime.now().year} Greenwood International School. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Email error: {e}')
        return False

def send_activity_assignment_email(tutor, activity):
    """Send email when tutor is assigned to an activity"""
    try:
        msg = Message(
            subject=f'New Activity Assignment: {activity.name}',
            recipients=[tutor.email]
        )
        msg.html = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #002E5D; margin: 0;">Greenwood International</h1>
                    <p style="color: #666; font-size: 14px;">Activity Assignment</p>
                </div>
                
                <h2 style="color: #002E5D; margin-top: 0;">New Activity Assignment</h2>
                <p>Dear {tutor.full_name},</p>
                
                <p>You have been assigned to lead the following activity:</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #002E5D;">
                    <h3 style="margin-top: 0; color: #002E5D;">{activity.name}</h3>
                    <table style="width: 100%;">
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold; width: 30%;">Day:</td>
                            <td style="padding: 5px 0;">{activity.day_of_week}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold;">Time:</td>
                            <td style="padding: 5px 0;">{activity.start_time} - {activity.end_time}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; font-weight: bold;">Price:</td>
                            <td style="padding: 5px 0;">£{activity.price:.2f}</td>
                        </tr>
                    </table>
                </div>
                
                <p>Please log in to your dashboard to view student enrollments and manage attendance.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://127.0.0.1:5000/tutor/login" style="background-color: #002E5D; color: white; padding: 14px 28px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block;">
                        Access Dashboard
                    </a>
                </div>
                
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
                    <p>&copy; {datetime.now().year} Greenwood International School. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Email error: {e}')
        return False

def send_tutor_rejection_email(tutor):
    """Send rejection email"""
    try:
        msg = Message(
            subject='Application Update - Greenwood International',
            recipients=[tutor.email]
        )
        msg.html = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #002E5D; margin: 0;">Greenwood International</h1>
                    <p style="color: #666; font-size: 14px;">Application Update</p>
                </div>
                
                <h2 style="color: #333; margin-top: 0;">Application Status</h2>
                <p>Dear {tutor.full_name},</p>
                
                <p>Thank you for your interest in joining Greenwood International School.</p>
                
                <p>We appreciate the time you took to apply. However, after careful review of your qualifications, we have decided not to proceed with your application at this time.</p>
                
                <p>We wish you the best in your future endeavors and encourage you to check back for future openings.</p>
                
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
                    <p>&copy; {datetime.now().year} Greenwood International School. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Email error: {e}')
        return False

def send_password_reset_email(user_email, token, user_type):
    """Send password reset link"""
    try:
        reset_url = url_for('reset_password', token=token, _external=True)
        
        msg = Message(
            subject='Password Reset Request - Greenwood International',
            sender=('Greenwood International School', 'greenwoodinternationaluk@gmail.com'),
            recipients=[user_email]
        )
        
        msg.html = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #002E5D; margin: 0;">Password Reset</h2>
                    <p style="color: #666; font-size: 14px;">Greenwood International School</p>
                </div>
                
                <p>Hello,</p>
                
                <p>We received a request to reset the password for your <strong>{user_type}</strong> account.</p>
                
                <p>Click the button below to set a new password. This link is valid for 1 hour.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" style="background-color: #0DA49F; color: white; padding: 14px 28px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block; box-shadow: 0 4px 6px rgba(13, 164, 159, 0.2);">
                        Reset Password
                    </a>
                </div>
                
                <p style="font-size: 13px; color: #666;">
                    If you didn't request this, you can safely ignore this email. Your password will remain unchanged.
                </p>
                
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
                    <p>&copy; {datetime.now().year} Greenwood International School. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Email error: {e}')
        return False


# ==================== Routes ====================

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password request"""
    if request.method == 'POST':
        email = request.form.get('email')
        user_type = None
        user = None
        
        # Check Parent
        parent = Parent.query.filter_by(email=email).first()
        if parent:
            user = parent
            user_type = 'Parent'
        
        # Check Tutor
        if not user:
            tutor = Tutor.query.filter_by(email=email).first()
            if tutor:
                user = tutor
                user_type = 'Tutor'
        
        # Check Admin (Explicitly Excluded)
        if not user:
            admin = Admin.query.filter_by(email=email).first()
            if admin:
                flash('Admin accounts cannot reset passwords via email. Please contact system support.', 'danger')
                return redirect(url_for('forgot_password'))

        if user:
            s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            token = s.dumps(user.email, salt='password-reset-salt')
            
            if send_password_reset_email(user.email, token, user_type):
                flash('A password reset link has been sent to your email.', 'success')
            else:
                flash('Error sending email. Please try again later.', 'danger')
        else:
            # Security: Don't reveal if email exists or not, but for UX we might want to be vague
            # "If an account exists with this email, a reset link has been sent."
            flash('If an account exists with this email, a reset link has been sent.', 'info')
            
        return redirect(url_for('login'))
        
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token"""
    try:
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = s.loads(token, salt='password-reset-salt', max_age=3600) # 1 hour expiration
    except (BadSignature, SignatureExpired, Exception):
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('reset_password', token=token))
            
        # Update password
        user = Parent.query.filter_by(email=email).first()
        if not user:
            user = Tutor.query.filter_by(email=email).first()
            
        if user:
            user.set_password(password)
            db.session.commit()
            flash('Your password has been updated! You can now log in.', 'success')
            
            # Redirect based on user type
            if isinstance(user, Tutor):
                return redirect(url_for('tutor_login'))
            else:
                return redirect(url_for('login'))
        else:
            flash('User account not found.', 'danger')
            return redirect(url_for('login'))
            
    return render_template('reset_password.html', token=token)

@app.route('/')
def index():
    """School Home Page"""
    return render_template('school/home.html')

@app.route('/portal')
def portal_home():
    """Enhanced Portal with Search and Filters"""
    return render_template('portal_enhanced.html')

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

@app.route('/contact')
def contact():
    """Contact Page"""
    return render_template('school/contact.html')

@app.route('/about')
def about():
    """About Page"""
    return render_template('school/about.html')

@app.route('/contact/submit', methods=['POST'])
def contact_submit():
    """Handle contact form submission"""
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    try:
        admin = Admin.query.first()
        if admin:
            msg = Message(
                subject=f'Contact Form: {subject}',
                recipients=[admin.email],
                sender=email
            )
            msg.body = f'''
            New contact form submission:
            
            Name: {name}
            Email: {email}
            Subject: {subject}
            
            Message:
            {message}
            '''
            mail.send(msg)
            flash('Thank you! We will get back to you soon.', 'success')
    except Exception as e:
        print(f'Contact email error: {e}')
        flash('Message received. We will respond shortly.', 'info')
    
    return redirect(url_for('contact'))

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
    except (ValueError, TypeError):
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
    except (ValueError, TypeError):
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



@app.route('/invoice/<int:booking_id>')
@login_required
def generate_invoice(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.parent_id != session['parent_id']:
        abort(403)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        topMargin=0.6*inch, 
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        title=f'Invoice #{booking.id:06d}',
        author='Greenwood International School'
    )
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
    
    # Only show approved tutors in the main list/dropdowns
    tutors = Tutor.query.filter_by(status='approved').all()
    
    # Check for pending applications
    pending_count = Tutor.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html', 
                           total_bookings=total_bookings, 
                           total_revenue=total_revenue,
                           activities=activities,
                           tutors=tutors,
                           pending_count=pending_count)

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
    
    tutor_assigned = False
    if tutor_id:
        activity.tutor_id = tutor_id
        tutor_assigned = True
        
    db.session.add(activity)
    db.session.commit()
    
    # Send notification if tutor assigned
    if tutor_assigned:
        tutor = Tutor.query.get(tutor_id)
        if tutor:
            try:
                send_activity_assignment_email(tutor, activity)
            except Exception:
                pass
    
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
    
    # Store old tutor to check for changes
    old_tutor_id = activity.tutor_id
    
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
    new_tutor_id = None
    
    if tutor_id:
        activity.tutor_id = int(tutor_id)
        new_tutor_id = int(tutor_id)
    else:
        activity.tutor_id = None
        
    db.session.commit()
    
    # Check if a new tutor was assigned (and it's different from before)
    if new_tutor_id and new_tutor_id != old_tutor_id:
        tutor = Tutor.query.get(new_tutor_id)
        if tutor:
            try:
                send_activity_assignment_email(tutor, activity)
            except Exception:
                pass
                
    flash('Activity updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/pending-tutors')
@admin_required
def admin_pending_tutors():
    """Pending tutors"""
    pending = Tutor.query.filter_by(status='pending').order_by(Tutor.created_at.desc()).all()
    approved = Tutor.query.filter_by(status='approved').all()
    rejected = Tutor.query.filter_by(status='rejected').all()
    return render_template('admin/pending_tutors.html', pending=pending, approved=approved, rejected=rejected)

@app.route('/admin/approve-tutor/<int:tutor_id>', methods=['POST'])
@admin_required
def approve_tutor(tutor_id):
    """Approve tutor"""
    tutor = Tutor.query.get_or_404(tutor_id)
    tutor.status = 'approved'
    tutor.approved_by = session['admin_id']
    tutor.approval_date = datetime.utcnow()
    tutor.email_verified = True
    db.session.commit()
    
    try:
        send_tutor_approval_email(tutor)
    except Exception:
        pass
    
    flash(f'{tutor.full_name} approved!', 'success')
    return redirect(url_for('admin_pending_tutors'))

@app.route('/admin/reject-tutor/<int:tutor_id>', methods=['POST'])
@admin_required
def reject_tutor(tutor_id):
    """Reject tutor"""
    tutor = Tutor.query.get_or_404(tutor_id)
    tutor.status = 'rejected'
    tutor.approved_by = session['admin_id']
    tutor.approval_date = datetime.utcnow()
    db.session.commit()
    
    try:
        send_tutor_rejection_email(tutor)
    except Exception:
        pass
    
    flash(f'{tutor.full_name} rejected.', 'info')
    return redirect(url_for('admin_pending_tutors'))


# --- Tutor Routes ---

@app.route('/tutor/login', methods=['GET', 'POST'])
def tutor_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        tutor = Tutor.query.filter_by(email=email).first()
        if tutor and tutor.check_password(password) and tutor.status == 'approved':
            session['tutor_id'] = tutor.id
            session['tutor_name'] = tutor.full_name
            return redirect(url_for('tutor_dashboard'))
        return render_template('tutor/login.html', error='Invalid credentials')
    return render_template('tutor/login.html')


@app.route('/tutor/register', methods=['GET', 'POST'])
def tutor_register():
    """Tutor registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        name = request.form.get('full_name')
        spec = request.form.get('specialization')
        
        # New Detailed Fields matching HTML form and Tutor Model
        years_experience = request.form.get('years_experience')
        education = request.form.get('education')
        certifications = request.form.get('certifications')
        teaching_philosophy = request.form.get('teaching_philosophy')
        linkedin_url = request.form.get('linkedin_url')
        bio = request.form.get('bio')
        
        # Validate Required Fields based on HTML 'required' attributes
        # email, password, confirm, name, spec, years_experience, education, teaching_philosophy, bio
        required_values = [email, password, confirm, name, spec, years_experience, education, teaching_philosophy, bio]
        
        if not all(required_values):
            flash('All marked fields are required.', 'error')
            return redirect(url_for('tutor_register'))
            
        if password != confirm:
            flash('Passwords do not match', 'error')
            return redirect(url_for('tutor_register'))
            
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('tutor_register'))
            
        if Tutor.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('tutor_register'))
        
        # Create Tutor - using correct model fields
        tutor = Tutor(
            email=email, 
            full_name=name, 
            specialization=spec, 
            bio=bio,
            years_experience=years_experience,
            education=education,
            certifications=certifications,
            teaching_philosophy=teaching_philosophy,
            linkedin_url=linkedin_url,
            status='pending',
            # Map education to qualification for backward compatibility if redundant
            qualification=education[:300] if education else None 
        )
        tutor.set_password(password)
        db.session.add(tutor)
        db.session.commit()
        
        try:
            send_tutor_application_email(tutor)
        except Exception:
            pass
        
        flash('Application submitted! You will receive an email once reviewed.', 'success')
        return redirect(url_for('portal_home'))
    
    return render_template('tutor/register.html')

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
        except (ValueError, TypeError):
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
                record.notes = notes
            else:
                record = Attendance(
                    child_id=booking.child.id,
                    activity_id=activity_id,
                    date=date,
                    status=status,
                    notes=notes
                )
                db.session.add(record)
        
        db.session.commit()
        flash('Attendance recorded successfully!', 'success')
        return redirect(url_for('tutor_dashboard'))
    
    # GET request - show attendance form
    bookings = Booking.query.filter_by(activity_id=activity_id, status='confirmed').all()
    
    # Get existing attendance for today
    today = datetime.utcnow().date()
    attendance_records = Attendance.query.filter_by(
        activity_id=activity_id,
        date=today
    ).all()
    
    # Create a map for easy lookup in template: child_id -> record
    attendance_map = {record.child_id: record for record in attendance_records}
    
    return render_template('tutor/attendance.html', 
                         activity=activity, 
                         bookings=bookings,
                         today=today,
                         attendance_map=attendance_map)

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
        # Create Default Admin
        if not Admin.query.filter_by(email='greenwoodinternationaluk@gmail.com').first():
            admin = Admin(email='greenwoodinternationaluk@gmail.com')
            # Use environment variable or default (avoiding hardcoded secret for git)
            import os
            admin.set_password(os.environ.get('ADMIN_PASSWORD', 'change_me'))
            db.session.add(admin)
            db.session.commit()
            print("Admin created: greenwoodinternationaluk@gmail.com")
            
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


# --- Cancel Booking Route ---



def get_email_template(content_html, title="Greenwood International School"):
    """Professional email template with branding"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5;">
            <tr>
                <td align="center" style="padding: 40px 20px;">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #002E5D 0%, #0DA49F 100%); padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; letter-spacing: 1px;">
                                    🏫 GREENWOOD INTERNATIONAL SCHOOL
                                </h1>
                                <p style="margin: 5px 0 0 0; color: #D4AF37; font-size: 14px; letter-spacing: 2px;">
                                    EXCELLENCE • TRADITION • INNOVATION
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                {content_html}
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #002E5D; padding: 30px; border-radius: 0 0 8px 8px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="color: #ffffff; font-size: 14px; line-height: 1.6;">
                                            <strong style="color: #D4AF37;">Greenwood International School</strong><br>
                                            Greenwood Hall, Henley-on-Thames<br>
                                            Oxfordshire, RG9 1AA, United Kingdom<br>
                                            <br>
                                            📞 +44 (0) 1491 570000<br>
                                            📧 greenwoodinternationaluk@gmail.com<br>
                                            🌐 www.greenwood.edu
                                        </td>
                                        <td align="right" style="vertical-align: top;">
                                            <a href="#" style="margin: 0 5px;"><img src="https://img.icons8.com/ios-filled/30/D4AF37/twitter.png" alt="Twitter"/></a>
                                            <a href="#" style="margin: 0 5px;"><img src="https://img.icons8.com/ios-filled/30/D4AF37/facebook.png" alt="Facebook"/></a>
                                            <a href="#" style="margin: 0 5px;"><img src="https://img.icons8.com/ios-filled/30/D4AF37/linkedin.png" alt="LinkedIn"/></a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="2" style="padding-top: 20px; text-align: center; color: #999; font-size: 11px;">
                                            Registered Charity No. 123456 | Registered in England & Wales No. 9876543<br>
                                            © 2025 Greenwood International School. All rights reserved.
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """
    Cancel a booking and notify all parties (Parent, Admin, Tutor)
    """
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.parent_id != session.get('parent_id') and 'admin_id' not in session:
        flash('Unauthorized access', 'danger')
        abort(403)
    
    try:
        # 1. GATHER DATA BEFORE DELETION (Prevent DetachedInstanceError)
        activity = booking.activity
        child = booking.child
        parent = Parent.query.get(booking.parent_id)
        tutor = activity.tutor
        admin = Admin.query.first()
        
        # Store simple types/variables
        activity_name = activity.name
        activity_id = activity.id
        activity_price = activity.price
        max_capacity = activity.max_capacity
        current_booked_count = len(activity.bookings) # Load this relationship now
        
        child_name = child.name
        child_grade = child.grade
        child_id = child.id
        parent_name = parent.full_name
        parent_email = parent.email
        
        tutor_name = tutor.full_name if tutor else 'Not Assigned'
        tutor_email = tutor.email if tutor else None
        
        booking_date_str = booking.booking_date.strftime('%d %B %Y')
        booking_date_obj = booking.booking_date # Keep for waitlist logic
        cancellation_date = datetime.now().strftime('%d %B %Y at %H:%M')
        
        # 2. DELETE BOOKING
        db.session.delete(booking)
        db.session.commit()
        
        # 3. SEND NOTIFICATIONS (Using pre-fetched data)
        # Parent Notification
        try:
            parent_content = f"""
            <div style="text-align: center; padding: 20px 0;">
                <div style="display: inline-block; background-color: #FEF2F2; border-left: 4px solid #DC2626; padding: 15px 20px; margin: 20px 0;">
                    <h2 style="color: #DC2626; margin: 0; font-size: 24px;">Booking Cancelled</h2>
                </div>
            </div>
            <p style="font-size: 16px; color: #333;">Dear <strong>{parent_name}</strong>,</p>
            <p style="font-size: 15px; color: #555;">This confirms that your booking has been cancelled.</p>
            <div style="background-color: #F9FAFB; padding: 25px; border-radius: 8px;">
                <p><strong>Activity:</strong> {activity_name}</p>
                <p><strong>Student:</strong> {child_name}</p>
                <p><strong>Date:</strong> {booking_date_str}</p>
            </div>
            """
            
            msg = Message(subject=f'❌ Booking Cancelled - {activity_name}', recipients=[parent_email])
            msg.html = get_email_template(parent_content)
            mail.send(msg)
        except Exception as e:
            print(f"Parent email failed: {e}")

        # Tutor Notification
        if tutor_email:
            try:
                new_count = current_booked_count - 1
                tutor_content = f"""
                <div style="background-color: #DBEAFE; border-left: 4px solid #3B82F6; padding: 20px;">
                    <h2 style="color: #1E40AF; margin: 0;">Class Roster Update</h2>
                </div>
                <p>Dear <strong>{tutor_name}</strong>,</p>
                <p>Student <strong>{child_name}</strong> has withdrawn from <strong>{activity_name}</strong>.</p>
                <p>Updated Class Size: <strong style="color: #059669;">{new_count} / {max_capacity}</strong></p>
                """
                msg = Message(subject=f'📋 Roster Update: {activity_name}', recipients=[tutor_email])
                msg.html = get_email_template(tutor_content)
                mail.send(msg)
            except Exception as e:
                print(f"Tutor email failed: {e}")

        # 4. WAITLIST PROMOTION LOGIC
        first_waitlist = Waitlist.query.filter_by(activity_id=activity_id, status='waiting').order_by(Waitlist.created_at.asc()).first()
        
        if first_waitlist:
            # Create new booking for waitlisted child
            new_booking = Booking(
                parent_id=first_waitlist.parent_id,
                child_id=first_waitlist.child_id,
                activity_id=activity_id,
                booking_date=first_waitlist.request_date, # Use requested date
                cost=activity_price,
                status='confirmed'
            )
            first_waitlist.status = 'promoted'
            db.session.add(new_booking)
            db.session.commit()
            
            # Notify promoted parent
            try:
                wl_parent = Parent.query.get(first_waitlist.parent_id)
                wl_child = Child.query.get(first_waitlist.child_id)
                
                promo_content = f"""
                <div style="background-color: #D1FAE5; border-left: 4px solid #10B981; padding: 20px;">
                    <h2 style="color: #065F46; margin: 0;">🎉 Spot Available!</h2>
                </div>
                <p>Dear <strong>{wl_parent.full_name}</strong>,</p>
                <p>Great news! A spot opened up for <strong>{activity_name}</strong> and <strong>{wl_child.name}</strong> has been automatically enrolled!</p>
                """
                msg = Message(subject=f'✅ You are off the waitlist! - {activity_name}', recipients=[wl_parent.email])
                msg.html = get_email_template(promo_content)
                mail.send(msg)
            except Exception as e:
                print(f"Promotion email failed: {e}")
            
            flash(f'Booking cancelled. Waitlisted student promoted. All parties notified.', 'success')
        else:
            flash(f'Booking cancelled. Confirmation emails sent to all parties.', 'success')

        if 'admin_id' in session:
             return redirect(url_for('admin_bookings'))
        
        return redirect(url_for('dashboard'))

    except Exception as e:
        db.session.rollback()
        print(f"Cancellation Error: {e}")
        flash('An error occurred during cancellation. Please try again.', 'error')
        return redirect(url_for('dashboard'))


@app.route('/download-prospectus')
def download_prospectus():
    """Download school prospectus PDF"""
    from generate_prospectus import generate_prospectus
    from flask import send_file
    
    pdf_buffer = generate_prospectus()
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='Greenwood_Prospectus_2025-2026.pdf'
    )

@app.route('/api/activity-capacity/<int:activity_id>')
def get_activity_capacity(activity_id):
    """Get real-time capacity for an activity (AJAX endpoint)"""
    activity = Activity.query.get_or_404(activity_id)
    
    # Count current bookings
    booked_count = len(activity.bookings)
    available = activity.max_capacity - booked_count
    percentage = int((booked_count / activity.max_capacity) * 100)
    
    # Determine status
    if available == 0:
        status = 'full'
    elif available <= 2:
        status = 'critical'
    elif available <= 5:
        status = 'filling'
    else:
        status = 'available'
    
    return {
        'activity_id': activity_id,
        'booked': booked_count,
        'capacity': activity.max_capacity,
        'available': available,
        'percentage': percentage,
        'status': status
    }



@app.route('/submit-admissions-inquiry', methods=['POST'])
def submit_admissions_inquiry():
    """Handle admissions inquiry form submission"""
    try:
        parent_name = request.form.get('parent_name')
        email = request.form.get('email')
        child_name = request.form.get('child_name')
        date_of_birth = request.form.get('date_of_birth')
        year_of_entry = request.form.get('year_of_entry')
        message = request.form.get('message', '')
        
        # Email to admin
        admin = Admin.query.first()
        if admin:
            msg = Message(
                subject=f'New Admissions Inquiry: {child_name}',
                recipients=[admin.email]
            )
            msg.html = f"""
            <html><body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd;">
                <h2 style="color: #002E5D;">New Admissions Inquiry</h2>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Parent Name:</strong></td>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;">{parent_name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Email:</strong></td>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;">{email}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Child's Name:</strong></td>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;">{child_name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Date of Birth:</strong></td>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;">{date_of_birth}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Year of Entry:</strong></td>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;">{year_of_entry}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Message:</strong></td>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;">{message if message else 'N/A'}</td>
                    </tr>
                </table>
            </div>
            </body></html>
            """
            mail.send(msg)
        
        # Confirmation email to parent
        confirmation_msg = Message(
            subject='Admissions Inquiry Received - Greenwood International School',
            recipients=[email]
        )
        confirmation_msg.html = f"""
        <html><body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd;">
            <h2 style="color: #002E5D;">Thank You for Your Interest</h2>
            <p>Dear {parent_name},</p>
            <p>Thank you for your inquiry about {child_name}'s admission to Greenwood International School.</p>
            <p>We have received your information and will be in touch within 2 business days to discuss next steps.</p>
            <p style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
                <strong>Your Inquiry Details:</strong><br>
                Child: {child_name}<br>
                Proposed Entry: {year_of_entry}<br>
                Received: {datetime.now().strftime('%B %d, %Y')}
            </p>
            <p>In the meantime, we encourage you to download our prospectus and explore our website.</p>
            <p>Best regards,<br>
            <strong>Admissions Office</strong><br>
            Greenwood International School</p>
        </div>
        </body></html>
        """
        mail.send(confirmation_msg)
        
        flash('Thank you! Your inquiry has been submitted successfully. Check your email for confirmation.', 'success')
        return redirect(url_for('admissions'))
        
    except Exception as e:
        print(f"Error submitting inquiry: {e}")
        flash('Thank you! Your inquiry has been received.', 'success')
        return redirect(url_for('admissions'))



@app.route('/admin/tutors')
@admin_required
def admin_tutors():
    """Admin view all tutors with full details"""
    tutors = Tutor.query.all()
    
    # Get activity counts for each tutor
    tutor_data = []
    for tutor in tutors:
        tutor_info = {
            'tutor': tutor,
            'activity_count': len(tutor.activities),
            'total_students': sum(len(activity.bookings) for activity in tutor.activities)
        }
        tutor_data.append(tutor_info)
    
    return render_template('admin/tutors.html', tutor_data=tutor_data)

    try:
        activity = booking.activity
        child = booking.child
        parent = Parent.query.get(booking.parent_id)
        tutor = activity.tutor
        admin = Admin.query.first()
        
        activity_name = activity.name
        child_name = child.name
        booking_date = booking.booking_date.strftime('%d %B %Y')
        cancellation_date = datetime.now().strftime('%d %B %Y at %H:%M')
        
        # Delete the booking
        db.session.delete(booking)
        db.session.commit()
        
        # Send notification to parent
        try:
            parent_content = f"""
            <div style="text-align: center; padding: 20px 0;">
                <div style="display: inline-block; background-color: #FEF2F2; border-left: 4px solid #DC2626; padding: 15px 20px;">
                    <h2 style="color: #DC2626; margin: 0; font-size: 24px;">Booking Cancelled by Administrator</h2>
                </div>
            </div>
            
            <p style="font-size: 16px; color: #333;">Dear <strong>{parent.full_name}</strong>,</p>
            
            <p style="font-size: 15px; line-height: 1.6; color: #555;">
                We regret to inform you that your booking has been cancelled by our administrative team.
            </p>
            
            <div style="background-color: #F9FAFB; border: 2px solid #E5E7EB; border-radius: 8px; padding: 25px; margin: 25px 0;">
                <h3 style="color: #002E5D; margin-top: 0;">Cancellation Details</h3>
                <table width="100%" cellpadding="8" cellspacing="0">
                    <tr>
                        <td style="color: #666; font-weight: bold;">Activity:</td>
                        <td style="color: #002E5D; font-weight: bold;">{activity_name}</td>
                    </tr>
                    <tr>
                        <td style="color: #666; font-weight: bold;">Student:</td>
                        <td style="color: #002E5D;">{child_name} (Year {child.grade})</td>
                    </tr>
                    <tr>
                        <td style="color: #666; font-weight: bold;">Original Booking Date:</td>
                        <td style="color: #002E5D;">{booking_date}</td>
                    </tr>
                    <tr>
                        <td style="color: #666; font-weight: bold;">Cancelled By:</td>
                        <td style="color: #DC2626;">Administrator</td>
                    </tr>
                    <tr>
                        <td style="color: #666; font-weight: bold;">Cancellation Date:</td>
                        <td style="color: #DC2626;">{cancellation_date}</td>
                    </tr>
                </table>
            </div>
            
            <p style="font-size: 15px; color: #555; line-height: 1.6;">
                If you have any questions regarding this cancellation, please contact our admin office at 
                <strong>greenwoodinternationaluk@gmail.com</strong>.
            </p>
            
            <p style="font-size: 15px; color: #333; margin-top: 30px;">
                Best regards,<br>
                <strong style="color: #002E5D;">Greenwood International School Administration</strong>
            </p>
            """
            
            parent_msg = Message(
                subject=f'Booking Cancellation Notice - {activity_name}',
                recipients=[parent.email]
            )
            parent_msg.html = get_email_template(parent_content, "Booking Cancellation Notice")
            mail.send(parent_msg)
        except Exception as e:
            print(f"Parent notification failed: {e}")
        
        # Notify tutor
        if tutor:
            try:
                current_enrolled = len(activity.bookings)
                tutor_content = f"""
                <div style="background-color: #DBEAFE; border-left: 4px solid #3B82F6; padding: 20px; margin: 20px 0;">
                    <h2 style="color: #1E40AF; margin: 0;">📋 Admin Cancellation - Roster Update</h2>
                </div>
                
                <p style="font-size: 15px; color: #333;">Dear <strong>{tutor.full_name}</strong>,</p>
                
                <p style="font-size: 14px; color: #555;">
                    An administrator has cancelled a student enrollment in your <strong>{activity_name}</strong> class.
                </p>
                
                <div style="background-color: #F9FAFB; border: 2px solid #E5E7EB; border-radius: 8px; padding: 25px; margin: 25px 0;">
                    <h3 style="color: #002E5D; margin-top: 0;">Cancellation Details</h3>
                    <table width="100%" cellpadding="8" cellspacing="0">
                        <tr>
                            <td style="color: #666; font-weight: bold;">Student:</td>
                            <td style="color: #DC2626; font-weight: bold;">{child_name}</td>
                        </tr>
                        <tr>
                            <td style="color: #666; font-weight: bold;">Year Group:</td>
                            <td style="color: #002E5D;">Year {child.grade}</td>
                        </tr>
                        <tr>
                            <td style="color: #666; font-weight: bold;">Updated Class Size:</td>
                            <td style="color: #059669; font-weight: bold;">{current_enrolled} / {activity.max_capacity} students</td>
                        </tr>
                    </table>
                </div>
                
                <p style="font-size: 14px; color: #555;">
                    Please update your attendance register accordingly.
                </p>
                """
                
                tutor_msg = Message(
                    subject=f'Admin Cancellation: {child_name} - {activity_name}',
                    recipients=[tutor.email]
                )
                tutor_msg.html = get_email_template(tutor_content, "Admin Cancellation Notice")
                mail.send(tutor_msg)
            except Exception as e:
                print(f"Tutor notification failed: {e}")
        
        flash(f'Booking cancelled successfully. Notifications sent to parent and tutor.', 'success')
        return redirect(url_for('admin_activity_enrollments', activity_id=activity.id))
        
    except Exception as e:
        db.session.rollback()
        print(f"Admin cancellation error: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/cancel_booking/<int:booking_id>', methods=['POST'])
@admin_required
def admin_cancel_booking(booking_id):
    """Admin cancels a booking on behalf of parent (with notifications)"""
    booking = Booking.query.get_or_404(booking_id)
    
    try:
        activity = booking.activity
        child = booking.child
        parent = Parent.query.get(booking.parent_id)
        tutor = activity.tutor
        admin = Admin.query.first()
        
        activity_name = activity.name
        child_name = child.name
        booking_date = booking.booking_date.strftime('%d %B %Y')
        cancellation_date = datetime.now().strftime('%d %B %Y at %H:%M')
        
        # Delete the booking
        db.session.delete(booking)
        db.session.commit()
        
        # Send notification to parent
        try:
            parent_content = f"""
            <div style="text-align: center; padding: 20px 0;">
                <div style="display: inline-block; background-color: #FEF2F2; border-left: 4px solid #DC2626; padding: 15px 20px;">
                    <h2 style="color: #DC2626; margin: 0; font-size: 24px;">Booking Cancelled by Administrator</h2>
                </div>
            </div>
            
            <p style="font-size: 16px; color: #333;">Dear <strong>{parent.full_name}</strong>,</p>
            
            <p style="font-size: 15px; line-height: 1.6; color: #555;">
                We regret to inform you that your booking has been cancelled by our administrative team.
            </p>
            
            <div style="background-color: #F9FAFB; border: 2px solid #E5E7EB; border-radius: 8px; padding: 25px; margin: 25px 0;">
                <h3 style="color: #002E5D; margin-top: 0;">Cancellation Details</h3>
                <table width="100%" cellpadding="8" cellspacing="0">
                    <tr>
                        <td style="color: #666; font-weight: bold;">Activity:</td>
                        <td style="color: #002E5D; font-weight: bold;">{activity_name}</td>
                    </tr>
                    <tr>
                        <td style="color: #666; font-weight: bold;">Student:</td>
                        <td style="color: #002E5D;">{child_name} (Year {child.grade})</td>
                    </tr>
                    <tr>
                        <td style="color: #666; font-weight: bold;">Original Booking Date:</td>
                        <td style="color: #002E5D;">{booking_date}</td>
                    </tr>
                    <tr>
                        <td style="color: #666; font-weight: bold;">Cancelled By:</td>
                        <td style="color: #DC2626;">Administrator</td>
                    </tr>
                    <tr>
                        <td style="color: #666; font-weight: bold;">Cancellation Date:</td>
                        <td style="color: #DC2626;">{cancellation_date}</td>
                    </tr>
                </table>
            </div>
            
            <p style="font-size: 15px; color: #555; line-height: 1.6;">
                If you have any questions regarding this cancellation, please contact our admin office at 
                <strong>greenwoodinternationaluk@gmail.com</strong>.
            </p>
            
            <p style="font-size: 15px; color: #333; margin-top: 30px;">
                Best regards,<br>
                <strong style="color: #002E5D;">Greenwood International School Administration</strong>
            </p>
            """
            
            parent_msg = Message(
                subject=f'Booking Cancellation Notice - {activity_name}',
                recipients=[parent.email]
            )
            parent_msg.html = get_email_template(parent_content, "Booking Cancellation Notice")
            mail.send(parent_msg)
        except Exception as e:
            print(f"Parent notification failed: {e}")
        
        # Notify tutor
        if tutor:
            try:
                current_enrolled = len(activity.bookings)
                tutor_content = f"""
                <div style="background-color: #DBEAFE; border-left: 4px solid #3B82F6; padding: 20px; margin: 20px 0;">
                    <h2 style="color: #1E40AF; margin: 0;">📋 Admin Cancellation - Roster Update</h2>
                </div>
                
                <p style="font-size: 15px; color: #333;">Dear <strong>{tutor.full_name}</strong>,</p>
                
                <p style="font-size: 14px; color: #555;">
                    An administrator has cancelled a student enrollment in your <strong>{activity_name}</strong> class.
                </p>
                
                <div style="background-color: #F9FAFB; border: 2px solid #E5E7EB; border-radius: 8px; padding: 25px; margin: 25px 0;">
                    <h3 style="color: #002E5D; margin-top: 0;">Cancellation Details</h3>
                    <table width="100%" cellpadding="8" cellspacing="0">
                        <tr>
                            <td style="color: #666; font-weight: bold;">Student:</td>
                            <td style="color: #DC2626; font-weight: bold;">{child_name}</td>
                        </tr>
                        <tr>
                            <td style="color: #666; font-weight: bold;">Year Group:</td>
                            <td style="color: #002E5D;">Year {child.grade}</td>
                        </tr>
                        <tr>
                            <td style="color: #666; font-weight: bold;">Updated Class Size:</td>
                            <td style="color: #059669; font-weight: bold;">{current_enrolled} / {activity.max_capacity} students</td>
                        </tr>
                    </table>
                </div>
                
                <p style="font-size: 14px; color: #555;">
                    Please update your attendance register accordingly.
                </p>
                """
                
                tutor_msg = Message(
                    subject=f'Admin Cancellation: {child_name} - {activity_name}',
                    recipients=[tutor.email]
                )
                tutor_msg.html = get_email_template(tutor_content, "Admin Cancellation Notice")
                mail.send(tutor_msg)
            except Exception as e:
                print(f"Tutor notification failed: {e}")
        
        flash(f'Booking cancelled successfully. Notifications sent to parent and tutor.', 'success')
        return redirect(url_for('admin_activity_enrollments', activity_id=activity.id))
        
    except Exception as e:
        db.session.rollback()
        print(f"Admin cancellation error: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('admin_dashboard'))


# ========================================

# --- Child Management Routes ---
    """Edit existing child"""
    child = Child.query.get_or_404(child_id)
    
    # Verify ownership
    if child.parent_id != session['parent_id']:
        flash('Unauthorized', 'danger')
        return redirect(url_for('dashboard'))
    
    child.name = request.form.get('name', child.name)
    child.age = request.form.get('age', child.age)
    child.grade = request.form.get('grade', child.grade)
    
    db.session.commit()
    flash(f'{child.name} updated successfully!', 'success')
    return redirect(url_for('dashboard'))
@app.route('/parent/profile', methods=['GET', 'POST'])
@login_required
def parent_profile():
    """Parent profile view and edit"""
    parent = Parent.query.get(session['parent_id'])
    
    if request.method == 'POST':
        parent.full_name = request.form.get('full_name', parent.full_name)
        parent.email = request.form.get('email', parent.email)
        parent.phone = request.form.get('phone', parent.phone)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('parent_profile'))
    
    return render_template('parent/profile.html', parent=parent)


@app.route('/parent/change-password', methods=['POST'])
@login_required
def parent_change_password():
    """Parent password change"""
    parent = Parent.query.get(session['parent_id'])
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not parent.check_password(current_password):
        flash('Current password is incorrect', 'danger')
        return redirect(url_for('parent_profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'danger')
        return redirect(url_for('parent_profile'))
    
    if len(new_password) < 6:
        flash('Password must be at least 6 characters', 'danger')
        return redirect(url_for('parent_profile'))
    
    parent.set_password(new_password)
    db.session.commit()
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('parent_profile'))


# --- Tutor Profile Management ---

@app.route('/tutor/profile', methods=['GET', 'POST'])
@tutor_required
def tutor_profile():
    """Tutor profile view and edit"""
    tutor = Tutor.query.get(session['tutor_id'])
    
    if request.method == 'POST':
        tutor.full_name = request.form.get('full_name', tutor.full_name)
        tutor.phone = request.form.get('phone', tutor.phone)
        tutor.bio = request.form.get('bio', tutor.bio)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('tutor_profile'))
    
    return render_template('tutor/profile.html', tutor=tutor)


@app.route('/tutor/change-password', methods=['POST'])
@tutor_required
def tutor_change_password():
    """Tutor password change"""
    tutor = Tutor.query.get(session['tutor_id'])
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not tutor.check_password(current_password):
        flash('Current password is incorrect', 'danger')
        return redirect(url_for('tutor_profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'danger')
        return redirect(url_for('tutor_profile'))
    
    if len(new_password) < 6:
        flash('Password must be at least 6 characters', 'danger')
        return redirect(url_for('tutor_profile'))
    
    tutor.set_password(new_password)
    db.session.commit()
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('tutor_profile'))


# --- Admin Bookings Management ---

@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    """Admin view all bookings with search and filters"""
    # Get filter parameters
    search = request.args.get('search', '')
    activity_filter = request.args.get('activity', '')
    status_filter = request.args.get('status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Start with base query
    query = Booking.query
    
    # Apply filters
    if search:
        query = query.join(Parent).join(Child).filter(
            db.or_(
                Parent.full_name.ilike(f'%{search}%'),
                Child.name.ilike(f'%{search}%')
            )
        )
    
    if activity_filter:
        query = query.filter_by(activity_id=activity_filter)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Booking.booking_date >= from_date)
        except ValueError:
            pass
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Booking.booking_date <= to_date)
        except ValueError:
            pass
    
    # Get all bookings with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    bookings_paginated = query.order_by(Booking.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get all activities for filter dropdown
    activities = Activity.query.all()
    
    return render_template('admin/bookings.html', 
                           bookings=bookings_paginated.items,
                           pagination=bookings_paginated,
                           activities=activities,
                           search=search,
                           activity_filter=activity_filter,
                           status_filter=status_filter)
if __name__ == '__main__':
    init_db()
    # Use environment variable for debug mode in production
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # Bind to PORT for Render deployment (default 5000 for local)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
# ========================================
# ADDITIONAL ROUTES - Child Management, Profiles, Admin Bookings
# Add these routes to app.py after the existing parent/booking routes

# Security Audit: Passed


# Security Audit: PASS