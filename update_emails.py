"""
Email Consistency Update Script
Updates all email references to greenwoodinternationaluk@gmail.com
"""
import re

# Files to update with their line-specific changes
updates = {
    'app.py': [
        ('noreply@greenwood.edu.uk', 'greenwoodinternationaluk@gmail.com'),
        ('info@greenwood.edu.uk', 'greenwoodinternationaluk@gmail.com'),
        ('@greenwood.edu.uk', '@greenwoodinternationaluk.gmail.com'),  # Calendar UIDs
        ('admissions@greenwood.edu', 'greenwoodinternationaluk@gmail.com'),
        ('info@greenwood.edu', 'greenwoodinternationaluk@gmail.com'),
    ],
    'config.py': [
        ('noreply@greenwood.edu.uk', 'greenwoodinternationaluk@gmail.com'),
    ],
    'templates/base.html': [
        ('admissions@greenwood.edu', 'greenwoodinternationaluk@gmail.com'),
    ],
    'templates/school/contact.html': [
        ('admissions@greenwood.edu', 'greenwoodinternationaluk@gmail.com'),
        ('info@greenwood.edu', 'greenwoodinternationaluk@gmail.com'),
    ],
}

def update_emails():
    """Update email addresses in all files"""
    import os
    base_path = r'c:\Users\Sanchit Kaushal\OneDrive\Desktop\Advanced Software Engineering\FInal Project and Report - Copy\School_Activity_Booking_System'
    
    for filename, replacements in updates.items():
        filepath = os.path.join(base_path, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️  {filename} not found, skipping...")
            continue
        
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply replacements
        original_content = content
        for old, new in replacements:
            content = content.replace(old, new)
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated {filename}")
        else:
            print(f"ℹ️  No changes needed in {filename}")

if __name__ == '__main__':
    print("🔄 Updating email addresses to greenwoodinternationaluk@gmail.com...")
    update_emails()
    print("\n✅ Email update complete!")
