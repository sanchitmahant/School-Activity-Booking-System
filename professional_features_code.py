"""
Professional Features Addition Script
This script adds all professional features to app.py in one go
"""

# Email helper functions to add after existing helper functions (around line 450)
EMAIL_FUNCTIONS = '''
# ==================== Email Notification Functions ====================

def send_tutor_application_email(tutor):
    """Send email notifications when a tutor applies"""
    try:
        # Email to tutor (confirmation)
        tutor_msg = Message(
            subject='Application Received - Greenwood International School',
            sender=('Greenwood International School', 'noreply@greenwood.edu.uk'),
            recipients=[tutor.email]
        )
        
        tutor_msg.html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #002E5D;">Application Received</h2>
                
                <p>Dear {tutor.full_name},</p>
                
                <p>Thank you for applying to become a tutor at Greenwood International School!</p>
                
                <p>Your application has been received and is currently under review by our administration team.</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #002E5D; margin-top: 0;">Application Details</h3>
                    <p><strong>Name:</strong> {tutor.full_name}</p>
                    <p><strong>Email:</strong> {tutor.email}</p>
                    <p><strong>Specialization:</strong> {tutor.specialization}</p>
                    <p><strong>Application Date:</strong> {tutor.application_date.strftime('%B %d, %Y')}</p>
                    <p><strong>Status:</strong> <span style="color: #ffc107;">Pending Review</span></p>
                </div>
                
                <p>You will receive an email notification once your application has been reviewed.</p>
                
                <p>If you have any questions, please contact us at greenwoodinternationaluk@gmail.com</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                    <p><strong>Greenwood International School</strong><br>
                    Greenwood Hall, Henley-on-Thames, Oxfordshire, RG9 1AA<br>
                    📧 greenwoodinternationaluk@gmail.com | 📞 +44 20 7123 4567</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Email to admin (notification)
        admin = Admin.query.first()
        if admin:
            admin_msg = Message(
                subject=f'New Tutor Application: {tutor.full_name}',
                sender=('Greenwood International School', 'noreply@greenwood.edu.uk'),
                recipients=[admin.email]
            )
            
            admin_msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #002E5D;">New Tutor Application</h2>
                    
                    <p>A new tutor has applied to join Greenwood International School.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="color: #002E5D; margin-top: 0;">Applicant Details</h3>
                        <p><strong>Name:</strong> {tutor.full_name}</p>
                        <p><strong>Email:</strong> {tutor.email}</p>
                        <p><strong>Specialization:</strong> {tutor.specialization}</p>
                        <p><strong>Qualifications:</strong> {tutor.qualifications[:200] if tutor.qualifications else 'Not provided'}...</p>
                    </div>
                    
                    <p style="background-color: #0d6efd; color: white; padding: 15px; text-align: center; border-radius: 5px;">
                        <a href="http://127.0.0.1:5000/admin/pending-tutors" style="color: white; text-decoration: none; font-weight: bold;">
                            Review Application →
                        </a>
                    </p>
                    
                    <p style="font-size: 12px; color: #666;">Login to the admin panel to review and approve/reject this application.</p>
                </div>
            </body>
            </html>
            """
            
            mail.send(admin_msg)
        
        mail.send(tutor_msg)
        return True
        
    except Exception as e:
        print(f'❌ Email sending failed: {str(e)}')
        return False


def send_tutor_approval_email(tutor):
    """Send email when tutor is approved"""
    try:
        msg = Message(
            subject='Application Approved - Welcome to Greenwood!',
            sender=('Greenwood International School', 'noreply@greenwood.edu.uk'),
            recipients=[tutor.email]
        )
        
        msg.html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #28a745;">🎉 Application Approved!</h2>
                
                <p>Dear {tutor.full_name},</p>
                
                <p>Congratulations! Your application to become a tutor at Greenwood International School has been <strong style="color: #28a745;">APPROVED</strong>!</p>
                
                <div style="background-color: #d4edda; border-left: 4px solid #28a745; padding: 20px; margin: 20px 0;">
                    <h3 style="color: #155724; margin-top: 0;">Next Steps</h3>
                    <p><strong style="color: #155724;">1.</strong> Login to your tutor portal at <a href="http://127.0.0.1:5000/tutor/login">http://127.0.0.1:5000/tutor/login</a></p>
                    <p><strong style="color: #155724;">2.</strong> Complete your profile with additional details</p>
                    <p><strong style="color: #155724;">3.</strong> View your assigned activities and upcoming sessions</p>
                    <p><strong style="color: #155724;">4.</strong> Start marking attendance for your students</p>
                </div>
                
                <p><strong>Your Login Credentials:</strong></p>
                <ul>
                    <li>Email: {tutor.email}</li>
                    <li>Password: [The password you set during registration]</li>
                </ul>
                
                <p>Welcome to the team! We look forward to your contributions to student excellence.</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                    <p><strong>Greenwood International School</strong><br>
                    Greenwood Hall, Henley-on-Thames, Oxfordshire, RG9 1AA<br>
                    📧 greenwoodinternationaluk@gmail.com | 📞 +44 20 7123 4567</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f'❌ Email sending failed: {str(e)}')
        return False


def send_tutor_rejection_email(tutor):
    """Send email when tutor is rejected"""
    try:
        msg = Message(
            subject='Application Update - Greenwood International School',
            sender=('Greenwood International School', 'noreply@greenwood.edu.uk'),
            recipients=[tutor.email]
        )
        
        msg.html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #002E5D;">Application Update</h2>
                
                <p>Dear {tutor.full_name},</p>
                
                <p>Thank you for your interest in becoming a tutor at Greenwood International School.</p>
                
                <p>After careful consideration, we regret to inform you that we are unable to proceed with your application at this time.</p>
                
                <p>This decision does not reflect on your qualifications or abilities. We receive many excellent applications and have to make difficult choices based on our current needs and capacity.</p>
                
                <p>We encourage you to reapply in the future when additional opportunities become available.</p>
                
                <p>Thank you again for your interest in Greenwood International School.</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                    <p><strong>Greenwood International School</strong><br>
                    📧 greenwoodinternationaluk@gmail.com | 📞 +44 20 7123 4567</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f'❌ Email sending failed: {str(e)}')
        return False
'''

# Tutor registration route
TUTOR_REGISTRATION_ROUTE = '''
# --- Tutor Registration ---

@app.route('/tutor/register', methods=['GET', 'POST'])
def tutor_register():
    """Public tutor registration form"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        specialization = request.form.get('specialization')
        qualifications = request.form.get('qualifications')
        bio = request.form.get('bio')
        
        # Validation
        if not all([email, password, confirm_password, full_name, specialization, qualifications]):
            return render_template('tutor/register.html', error='All required fields must be completed')
        
        # Email validation
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return render_template('tutor/register.html', error='Invalid email address format')
        
        # Password strength
        if len(password) < 8:
            return render_template('tutor/register.html', error='Password must be at least 8 characters long')
        
        if password != confirm_password:
            return render_template('tutor/register.html', error='Passwords do not match')
        
        # Check if email already exists
        if Tutor.query.filter_by(email=email).first():
            return render_template('tutor/register.html', error='Email already registered')
        
        # Create pending tutor account
        tutor = Tutor(
            email=email,
            full_name=full_name,
            specialization=specialization,
            qualifications=qualifications,
            bio=bio,
            status='pending'
        )
        tutor.set_password(password)
        db.session.add(tutor)
        db.session.commit()
        
        # Send notification emails
        try:
            send_tutor_application_email(tutor)
            print(f'✅ Application emails sent for {tutor.email}')
        except Exception as e:
            print(f'⚠️ Email sending failed: {str(e)}')
        
        flash('Application submitted successfully! You will receive an email once your application is reviewed.', 'success')
        return redirect(url_for('portal_home'))
    
    return render_template('tutor/register.html')
'''

# Admin pending tutors routes
ADMIN_TUTOR_ROUTES = '''
# --- Admin Tutor Management ---

@app.route('/admin/pending-tutors')
@admin_required
def admin_pending_tutors():
    """View all pending tutor applications"""
    pending_tutors = Tutor.query.filter_by(status='pending').order_by(Tutor.application_date.desc()).all()
    approved_tutors = Tutor.query.filter_by(status='approved').order_by(Tutor.approval_date.desc()).all()
    rejected_tutors = Tutor.query.filter_by(status='rejected').order_by(Tutor.approval_date.desc()).all()
    
    return render_template('admin/pending_tutors.html', 
                         pending=pending_tutors,
                         approved=approved_tutors,
                         rejected=rejected_tutors)

@app.route('/admin/approve-tutor/<int:tutor_id>', methods=['POST'])
@admin_required
def approve_tutor(tutor_id):
    """Approve a tutor application"""
    tutor = Tutor.query.get_or_404(tutor_id)
    
    tutor.status = 'approved'
    tutor.approved_by = session['admin_id']
    tutor.approval_date = datetime.utcnow()
    tutor.email_verified = True
    
    db.session.commit()
    
    # Send approval email
    try:
        send_tutor_approval_email(tutor)
        print(f'✅ Approval email sent to {tutor.email}')
    except Exception as e:
        print(f'⚠️ Email sending failed: {str(e)}')
    
    flash(f'Tutor {tutor.full_name} has been approved!', 'success')
    return redirect(url_for('admin_pending_tutors'))

@app.route('/admin/reject-tutor/<int:tutor_id>', methods=['POST'])
@admin_required
def reject_tutor(tutor_id):
    """Reject a tutor application"""
    tutor = Tutor.query.get_or_404(tutor_id)
    
    tutor.status = 'rejected'
    tutor.approved_by = session['admin_id']
    tutor.approval_date = datetime.utcnow()
    
    db.session.commit()
    
    # Send rejection email
    try:
        send_tutor_rejection_email(tutor)
        print(f'✅ Rejection email sent to {tutor.email}')
    except Exception as e:
        print(f'⚠️ Email sending failed: {str(e)}')
    
    flash(f'Tutor {tutor.full_name} application has been rejected.', 'info')
    return redirect(url_for('admin_pending_tutors'))
'''

print("✅ Professional features code generated!")
print("\nNext steps:")
print("1. Add EMAIL_FUNCTIONS to app.py (around line 450)")
print("2. Add TUTOR_REGISTRATION_ROUTE to app.py (around line 540)")
print("3. Add ADMIN_TUTOR_ROUTES to app.py (after admin routes)")
print("4. Create template files")
print("5. Update tutor login to check approval status")
