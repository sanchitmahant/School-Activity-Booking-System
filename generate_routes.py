"""
Add Enhanced Portal and PDF Routes to app.py
Safe addition without modifying existing code
"""

# Routes to add to app.py

PORTAL_ROUTE = """
@app.route('/portal')
def portal_home():
    \"\"\"Enhanced Portal with Search and Filters\"\"\"
    return render_template('portal_enhanced.html')
"""

CONTACT_ROUTE = """
@app.route('/contact')
def contact():
    \"\"\"Contact Page\"\"\"
    return render_template('school/contact.html')
"""

ABOUT_ROUTE = """
@app.route('/about')
def about():
    \"\"\"About Page\"\"\"
    return render_template('school/about.html')
"""

CONTACT_SUBMIT_ROUTE = """
@app.route('/contact/submit', methods=['POST'])
def contact_submit():
    \"\"\"Handle contact form submission\"\"\"
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
"""

PDF_IMPORT = """
# Enhanced PDF Invoice Generator
from enhanced_invoice import get_enhanced_invoice_pdf
"""

INSTRUCTIONS = """
=== MANUAL INTEGRATION INSTRUCTIONS ===

Add these to your app.py file:

1. ADD IMPORT (near top of file, with other imports):
-------------------------------------------------------
from enhanced_invoice import get_enhanced_invoice_pdf


2. ADD ROUTES (after existing school routes, around line 550-600):
-------------------------------------------------------------------
""" + PORTAL_ROUTE + CONTACT_ROUTE + ABOUT_ROUTE + CONTACT_SUBMIT_ROUTE + """

3. UPDATE INVOICE GENERATOR (find the generate_invoice function):
------------------------------------------------------------------
Replace the PDF generation part with:
    pdf_buffer = get_enhanced_invoice_pdf(booking)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Invoice_GRN{booking.id:06d}_Greenwood.pdf'
    )

====================================================================
NOTE: Since app.py structure varies, these are provided as snippets.
Copy and paste them into the appropriate locations in your app.py.
====================================================================
"""

if __name__ == '__main__':
    print(INSTRUCTIONS)
    
    # Save to a text file for easy reference
    with open('ROUTES_TO_ADD.txt', 'w') as f:
        f.write(INSTRUCTIONS)
    
    print("\n✅ Instructions saved to ROUTES_TO_ADD.txt")
