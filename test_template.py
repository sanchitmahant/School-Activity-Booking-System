"""Quick script to check if admin dashboard loads without errors"""
from app import app

with app.app_context():
    from flask import render_template
    try:
        # Try to render the template to check for syntax errors
        html = render_template('admin/dashboard.html', 
                              total_bookings=0, 
                              total_revenue=0, 
                              activities=[], 
                              tutors=[])
        print("✓ Template renders successfully!")
        print(f"Length: {len(html)} characters")
    except Exception as e:
        print(f"✗ Template Error: {e}")
