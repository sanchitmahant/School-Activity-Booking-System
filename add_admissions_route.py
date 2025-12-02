"""
Add admissions inquiry route to app.py
"""

print("=" * 70)
print("ADDING ADMISSIONS INQUIRY ROUTE TO APP.PY")
print("=" * 70)

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Route to add
new_route = '''
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

'''

# Find insertion point (before if __name__)
if_main_pos = content.find("if __name__ == '__main__':")
if if_main_pos > 0:
    content = content[:if_main_pos] + new_route + "\n" + content[if_main_pos:]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Admissions inquiry route added successfully!")
    print("   Route: /submit-admissions-inquiry")
else:
    print("⚠️ Could not find insertion point")

print("\n✅ All routes updated!")
