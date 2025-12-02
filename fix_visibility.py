"""
Fix Hero Text Visibility & Add Alumni Photos
Updates all hero sections for better contrast and adds professional alumni profiles
"""
import re

def fix_contrast_issues():
    """Fix low-contrast hero headings across all pages"""
    
    fixes = {
        'templates/school/home.html': [
            # Fix "Inspiring Excellence" heading
            (r'<h1 class="display-3 fw-bold mb-4" style="line-height: 1\.2;">',
             '<h1 class="display-3 fw-bold mb-4" style="line-height: 1.2; color: white;">'),
            # Fix "Ready to Get Started" heading  
            (r'<h2 class="display-5 fw-bold mb-4">Ready to Get Started\?</h2>',
             '<h2 class="display-5 fw-bold mb-4" style="color: white;">Ready to Get Started?</h2>'),
        ],
        'templates/school/academic.html': [
            # Fix "Academic Excellence" heading
            (r'<h1 class="display-3 fw-bold mb-4" data-aos="fade-up">Academic Excellence</h1>',
             '<h1 class="display-3 fw-bold mb-4" style="color: white;" data-aos="fade-up">Academic Excellence</h1>'),
        ],
        'templates/school/admissions.html': [
            # Fix "Join Greenwood International" heading
            (r'<h1 class="display-3 fw-bold mb-4">Join Greenwood International</h1>',
             '<h1 class="display-3 fw-bold mb-4" style="color: white;">Join Greenwood International</h1>'),
        ],
    }
    
    import os
    base_path = r'c:\Users\Sanchit Kaushal\OneDrive\Desktop\Advanced Software Engineering\FInal Project and Report - Copy\School_Activity_Booking_System'
    
    for filepath, replacements in fixes.items():
        full_path = os.path.join(base_path, filepath)
        
        if not os.path.exists(full_path):
            print(f"⚠️  {filepath} not found")
            continue
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed contrast in {filepath}")
        else:
            print(f"ℹ️  No changes needed in {filepath}")

if __name__ == '__main__':
    print("🔧 Fixing hero text visibility...")
    fix_contrast_issues()
    print("\n✅ Contrast fixes complete! Refresh your browser to see changes.")
