"""
Add Activity Enrollment Management for Admin
Professional enrollment viewing and management with cancellation controls
"""

print("=" * 80)
print("ADDING PROFESSIONAL ENROLLMENT MANAGEMENT")
print("=" * 80)

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# New admin enrollment management routes
enrollment_routes = '''
@app.route('/admin/activity/<int:activity_id>/enrollments')
@admin_required
def admin_activity_enrollments(activity_id):
    """View all enrollments for a specific activity with management options"""
    activity = Activity.query.get_or_404(activity_id)
    
    # Get all bookings with parent and child details
    bookings = Booking.query.filter_by(activity_id=activity_id).all()
    
    enrollment_data = []
    for booking in bookings:
        data = {
            'booking': booking,
            'child': Child.query.get(booking.child_id),
            'parent': Parent.query.get(booking.parent_id)
        }
        enrollment_data.append(data)
    
    # Sort by booking date (most recent first)
    enrollment_data.sort(key=lambda x: x['booking'].booking_date, reverse=True)
    
    return render_template('admin/activity_enrollments.html',
                         activity=activity,
                         enrollment_data=enrollment_data,
                         total_enrolled=len(bookings),
                         available_spots=activity.max_capacity - len(bookings))

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
'''

# Find insertion point (before if __name__)
if_main_pos = content.find("if __name__ == '__main__':")
if if_main_pos > 0:
    content = content[:if_main_pos] + enrollment_routes + "\n\n" + content[if_main_pos:]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Admin enrollment management routes added!")
    print("   - /admin/activity/<id>/enrollments - View all enrolled students")
    print("   - /admin/cancel_booking/<id> - Admin cancel with notifications")
else:
    print("⚠️ Could not find insertion point")

print("\n✅ Enrollment management system configured!")
print("=" * 80)
