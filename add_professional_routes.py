"""
Add professional features routes to app.py
- Prospectus download
- Real-time capacity API
- School routes
"""
import os

print("=" * 70)
print("ADDING PROFESSIONAL FEATURES TO APP.PY")
print("=" * 70)

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Routes to add before "if __name__ == '__main__':"
new_routes = '''
# ==================== Professional School Features ====================

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

'''

# Find insertion point (before if __name__)
if_main_pos = content.find("if __name__ == '__main__':")
if if_main_pos > 0:
    # Insert routes before if __name__
    content = content[:if_main_pos] + new_routes + "\n" + content[if_main_pos:]
    print("✅ Added professional school routes")
    
    # Write back
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ app.py updated successfully!")
else:
    print("⚠️ Could not find insertion point")

print("\n📋 Routes Added:")
print("   - /download-prospectus - Download PDF prospectus")
print("   - /api/activity-capacity/<id> - Real-time capacity API")
