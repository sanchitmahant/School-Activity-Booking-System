"""
Quick script to add pending tutors link to admin dashboard
"""

# Read admin dashboard
with open('templates/admin/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add link after stats row (after line 60)
insert_text = '''
    <!-- Quick Actions -->
    <div class="row g-4 mb-5">
        <div class="col-md-12">
            <div class="card shadow-sm border-0 bg-light">
                <div class="card-body">
                    <h5 class="mb-3"><i class="fas fa-bolt"></i> Quick Actions</h5>
                    <a href="{{ url_for('admin_pending_tutors') }}" class="btn btn-warning me-2">
                        <i class="fas fa-user-clock"></i> Pending Tutor Applications
                    </a>
                    <a href="{{ url_for('tutor_register') }}" class="btn btn-outline-primary">
                        <i class="fas fa-user-plus"></i> Public Tutor Application Link
                    </a>
                </div>
            </div>
        </div>
    </div>
'''

# Find where to insert (after stats row closing div)
insert_pos = content.find("    </div>\r\n\r\n    <!-- Activity Management -->")
if insert_pos > 0:
    content = content[:insert_pos + 10] + "\r\n" + insert_text + content[insert_pos + 10:]
    print("✅ Added quick actions to admin dashboard")
else:
    print("⚠️  Could not find insertion point")

# Write back
with open('templates/admin/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Admin dashboard updated!")
