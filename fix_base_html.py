"""
Automated fix for base.html
Ensures missing_classes.css is properly linked and file structure is correct
"""

import os
import re

print("=" * 70)
print("FIXING BASE.HTML AUTOMATICALLY")
print("=" * 70)

base_html_path = 'templates/base.html'

# Read the original base.html from git
import subprocess
result = subprocess.run(['git', 'show', 'fed4b46:templates/base.html'], 
                       capture_output=True, text=True)

if result.returncode == 0:
    original_content = result.stdout
    
    # Find the line with style.css and add missing_classes.css after it
    lines = original_content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        if 'style.css' in line and 'missing_classes' not in line:
            # Add the missing CSS link right after style.css
            indent = '    '
            new_lines.append(f'{indent}<link rel="stylesheet" href="{{{{ url_for(\'static\', filename=\'css/missing_classes.css\') }}}}">')
    
    # Write the corrected content
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ base.html fixed successfully!")
    print("✅ missing_classes.css link added")
else:
    print("⚠️ Could not restore from git, using manual fix...")
    
    # Check if file exists and has content
    if os.path.exists(base_html_path):
        with open(base_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has the link
        if 'missing_classes.css' not in content:
            # Find style.css and add after it
            content = content.replace(
                'url_for(\'static\', filename=\'css/style.css\')',
                'url_for(\'static\', filename=\'css/style.css\') }}">\n    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/missing_classes.css\''
            )
            
            with open(base_html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Fixed using manual method")
        else:
            print("✅ Already has missing_classes.css link")

print("\n📋 Verification:")
print(f"   - File: {base_html_path}")
print(f"   - Size: {os.path.getsize(base_html_path)} bytes")
