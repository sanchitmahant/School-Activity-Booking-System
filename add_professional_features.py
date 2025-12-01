"""
Comprehensive script to add all professional features to the School Activity Booking System
Adds tutor registration, admin approval, enhanced emails, and templates
"""
import os
import shutil
from datetime import datetime

print("=" * 70)
print("PROFESSIONAL FEATURES INSTALLATION SCRIPT")
print("=" * 70)
print()

# Create backup
print("📦 Creating backup of app.py...")
shutil.copy('app.py', f'app.py.backup.{datetime.now().strftime("%Y%m%d%H%M%S")}')
print("✅ Backup created")

# Read current app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Email functions to add (after line 450, before routes)
EMAIL_FUNCTIONS = '''
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
        <html><body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd;">
            <h2 style="color: #002E5D;">Application Received</h2>
            <p>Dear {tutor.full_name},</p>
            <p>Thank you for applying to Greenwood International School!</p>
            <p>Your application is under review. You'll receive an email once reviewed.</p>
            <p style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
                <strong>Application Date:</strong> {tutor.application_date.strftime('%B %d, %Y')}<br>
                <strong>Status:</strong> <span style="color: #ffc107;">Pending Review</span>
            </p>
        </div>
        </body></html>
        """
        
        # Admin notification
        admin = Admin.query.first()
        if admin:
            admin_msg = Message(
                subject=f'New Tutor Application: {tutor.full_name}',
                recipients=[admin.email]
            )
            admin_msg.html = f"""
            <html><body style="font-family: Arial;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2>New Tutor Application</h2>
                <p><strong>Name:</strong> {tutor.full_name}</p>
                <p><strong>Email:</strong> {tutor.email}</p>
                <p><strong>Specialization:</strong> {tutor.specialization}</p>
                <p style="background: #0d6efd; color: white; padding: 15px; text-align: center;">
                    <a href="http://127.0.0.1:5000/admin/pending-tutors" style="color: white; text-decoration: none;">
                        Review Application →
                    </a>
                </p>
            </div>
            </body></html>
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
        <html><body style="font-family: Arial;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #28a745;">🎉 Application Approved!</h2>
            <p>Dear {tutor.full_name},</p>
            <p>Your application has been <strong style="color: #28a745;">APPROVED</strong>!</p>
            <p>Login at <a href="http://127.0.0.1:5000/tutor/login">Tutor Portal</a></p>
            <p>Welcome to the team!</p>
        </div>
        </body></html>
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
        <html><body style="font-family: Arial;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>Application Update</h2>
            <p>Dear {tutor.full_name},</p>
            <p>Thank you for your interest. After review, we are unable to proceed with your application at this time.</p>
            <p>You may reapply in the future.</p>
        </div>
        </body></html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Email error: {e}')
        return False

'''

# Tutor registration route
TUTOR_REGISTER_ROUTE = '''
@app.route('/tutor/register', methods=['GET', 'POST'])
def tutor_register():
    """Tutor registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        name = request.form.get('full_name')
        spec = request.form.get('specialization')
        quals = request.form.get('qualifications')
        bio = request.form.get('bio')
        
        if not all([email, password, confirm, name, spec, quals]):
            return render_template('tutor/register.html', error='All fields required')
        
        if password != confirm:
            return render_template('tutor/register.html', error='Passwords do not match')
        
        if len(password) < 8:
            return render_template('tutor/register.html', error='Password must be 8+ characters')
        
        if Tutor.query.filter_by(email=email).first():
            return render_template('tutor/register.html', error='Email already registered')
        
        tutor = Tutor(email=email, full_name=name, specialization=spec, qualifications=quals, bio=bio, status='pending')
        tutor.set_password(password)
        db.session.add(tutor)
        db.session.commit()
        
        try:
            send_tutor_application_email(tutor)
        except:
            pass
        
        flash('Application submitted! You will receive an email once reviewed.', 'success')
        return redirect(url_for('portal_home'))
    
    return render_template('tutor/register.html')

'''

# Admin routes
ADMIN_ROUTES = '''
@app.route('/admin/pending-tutors')
@admin_required
def admin_pending_tutors():
    """Pending tutors"""
    pending = Tutor.query.filter_by(status='pending').order_by(Tutor.application_date.desc()).all()
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
    except:
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
    except:
        pass
    
    flash(f'{tutor.full_name} rejected.', 'info')
    return redirect(url_for('admin_pending_tutors'))

'''

# Find insertion points and add code
print("\n📝 Adding professional features...")

# Add email functions before routes section
if "def send_tutor_application_email" not in content:
    # Find where to insert (after send_booking_confirmation_email function)
    insert_pos = content.find("# ==================== Routes ====================")
    if insert_pos > 0:
        content = content[:insert_pos] + EMAIL_FUNCTIONS + "\n" + content[insert_pos:]
        print("✅ Added email notification functions")
    else:
        print("⚠️  Could not find insertion point for email functions")

# Add tutor registration route
if "def tutor_register" not in content:
    # Insert after tutor login route
    insert_pos = content.find("@app.route('/tutor/login'")
    if insert_pos > 0:
        # Find end of tutor_login function
        next_route = content.find("\n@app.route", insert_pos + 10)
        if next_route > 0:
            content = content[:next_route] + "\n" + TUTOR_REGISTER_ROUTE + content[next_route:]
            print("✅ Added tutor registration route")
    else:
        print("⚠️  Could not find insertion point for tutor registration")

# Add admin tutor management routes
if "def admin_pending_tutors" not in content:
    # Insert after admin routes
    insert_pos = content.find("@app.route('/admin/dashboard'")
    if insert_pos > 0:
        next_section = content.find("\n# ---", insert_pos + 10)
        if next_section > 0:
            content = content[:next_section] + "\n" + ADMIN_ROUTES + content[next_section:]
            print("✅ Added admin tutor management routes")
    else:
        print("⚠️  Could not find insertion point for admin routes")

# Update tutor login to check approval status
if "tutor.status == 'approved'" not in content:
    # Find tutor login function and add status check
    tutor_login_start = content.find("def tutor_login():")
    if tutor_login_start > 0:
        # Find the line where tutor password is checked
        check_pos = content.find("if tutor and tutor.check_password(password):", tutor_login_start)
        if check_pos > 0:
            # Replace with approval check
            old_check = "if tutor and tutor.check_password(password):"
            new_check = "if tutor and tutor.check_password(password) and tutor.status == 'approved':"
            content = content.replace(old_check, new_check, 1)
            
            # Add error message for pending/rejected
            session_set = content.find("session['tutor_id'] = tutor.id", check_pos)
            if session_set > 0:
                # Find the else block
                else_block = content.find("else:", session_set)
                if else_block > 0:
                    old_error = "return render_template('tutor/login.html', error='Invalid email or password')"
                    new_error = """# Check if tutor exists but not approved
        if tutor and tutor.check_password(password) and tutor.status != 'approved':
            if tutor.status == 'pending':
                return render_template('tutor/login.html', error='Your application is pending admin approval')
            else:
                return render_template('tutor/login.html', error='Your application was not approved')
        return render_template('tutor/login.html', error='Invalid email or password')"""
                    content = content.replace(old_error, new_error, 1)
            
            print("✅ Updated tutor login with approval check")

# Write updated app.py
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ app.py updated successfully!")
print(f"\n📋 Summary:")
print(f"   - Email notification functions added")
print(f"   - Tutor registration route added")
print(f"   - Admin approval routes added")
print(f"   - Tutor login updated with status check")
print(f"\n⚠️  Next: Create template files for the new pages")
