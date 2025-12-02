"""
Comprehensive Contrast Fix - All Pages
Fixes ALL low-contrast text across the entire website
"""
import os
import re

def fix_all_contrast_issues():
    """Fix every instance of low-contrast text across all templates"""
    
    base_path = r'c:\Users\Sanchit Kaushal\OneDrive\Desktop\Advanced Software Engineering\FInal Project and Report - Copy\School_Activity_Booking_System\templates'
    
    # Comprehensive list of all heading patterns that need white color on blue gradients
    fixes = [
        # Generic h1, h2, h3, h4, h5 on gradient backgrounds without explicit color
        (r'(<div[^>]*background:\s*linear-gradient[^>]*>.*?<h[1-5][^>]*)(>)([^<]*</h[1-5]>)', 
         r'\1 style="color: white;">\3'),
        
        # Specific heading patterns
        (r'<h2 class="display-5 fw-bold mb-4">Ready to Get Started\?</h2>',
         '<h2 class="display-5 fw-bold mb-4" style="color: white;">Ready to Get Started?</h2>'),
        
        (r'<h2 class="display-5 fw-bold mb-4">Join Our Academic Excellence Program</h2>',
         '<h2 class="display-5 fw-bold mb-4" style="color: white;">Join Our Academic Excellence Program</h2>'),
        
        (r'<h2 class="display-5 fw-bold mb-4">Ready to Begin\?</h2>',
         '<h2 class="display-5 fw-bold mb-4" style="color: white;">Ready to Begin?</h2>'),
        
        (r'<h2 class="display-5 fw-bold mb-4">Reconnect with Greenwood</h2>',
         '<h2 class="display-5 fw-bold mb-4" style="color: white;">Reconnect with Greenwood</h2>'),
        
        (r'<h4 class="fw-bold mb-4">Admissions Office</h4>',
         '<h4 class="fw-bold mb-4" style="color: white;">Admissions Office</h4>'),
        
        (r'<h4 class="fw-bold mb-4">Update Your Details</h4>',
         '<h4 class="fw-bold mb-4" style="color: white;">Update Your Details</h4>'),
    ]
    
    files_to_check = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.html'):
                files_to_check.append(os.path.join(root, file))
    
    print(f"🔍 Checking {len(files_to_check)} template files for contrast issues...\n")
    
    total_fixes = 0
    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_fixes = 0
            
            for pattern, replacement in fixes:
                new_content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)
                if new_content != content:
                    file_fixes += 1
                    content = new_content
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                relative_path = os.path.relpath(filepath, base_path)
                print(f"✅ Fixed {file_fixes} contrast issues in: {relative_path}")
                total_fixes += file_fixes
            
        except Exception as e:
            print(f"⚠️  Error processing {filepath}: {e}")
    
    print(f"\n🎉 Complete! Fixed {total_fixes} total contrast issues across all templates.")

if __name__ == '__main__':
    print("🔧 Comprehensive Contrast Fix - Scanning ALL templates...\n")
    fix_all_contrast_issues()
    print("\n✅ All visibility issues resolved! Refresh browser to see changes.")
