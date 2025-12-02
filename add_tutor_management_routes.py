"""
Add Tutor Management Routes to Admin Panel
Comprehensive tutor viewing and management for administrators
"""

print("=" * 80)
print("ADDING TUTOR MANAGEMENT TO ADMIN PANEL")
print("=" * 80)

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# New admin tutor management routes
tutor_management_routes = '''
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

@app.route('/admin/tutor/<int:tutor_id>')
@admin_required
def admin_tutor_detail(tutor_id):
    """View detailed tutor profile with qualifications and activities"""
    tutor = Tutor.query.get_or_404(tutor_id)
    
    # Get all activities by this tutor with booking counts
    activity_stats = []
    for activity in tutor.activities:
        stats = {
            'activity': activity,
            'booked': len(activity.bookings),
            'capacity': activity.max_capacity,
            'revenue': activity.price * len(activity.bookings)
        }
        activity_stats.append(stats)
    
    total_revenue = sum(stat['revenue'] for stat in activity_stats)
    total_students = sum(stat['booked'] for stat in activity_stats)
    
    return render_template('admin/tutor_detail.html', 
                         tutor=tutor,
                         activity_stats=activity_stats,
                         total_revenue=total_revenue,
                         total_students=total_students)
'''

# Find insertion point (after pending_tutors routes)
import re
pattern = r"(@app\.route\('/admin/reject_tutor.*?return redirect.*?\n)"
match = re.search(pattern, content, re.DOTALL)

if match:
    insert_pos = match.end()
    content = content[:insert_pos] + "\n" + tutor_management_routes + "\n" + content[insert_pos:]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Tutor management routes added!")
    print("   - /admin/tutors - View all tutors")
    print("   - /admin/tutor/<id> - Detailed tutor profile")
else:
    print("⚠️ Could not find insertion point, trying alternative...")
    # Try inserting before if __name__
    if_main_pos = content.find("if __name__ == '__main__':")
    if if_main_pos > 0:
        content = content[:if_main_pos] + tutor_management_routes + "\n\n" + content[if_main_pos:]
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Routes added (alternative method)")

print("\n✅ Admin tutor management routes configured!")
print("=" * 80)
