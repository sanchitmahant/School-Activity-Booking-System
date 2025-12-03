import csv

INPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'
OUTPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'

# Keywords that should NOT be classified as features
NON_FEATURE_KEYWORDS = [
    'ui', 'login', 'registration', 'register', 'sign up', 'sign in',
    'authentication', 'user interface', 'design', 'styling', 'css',
    'layout', 'responsive', 'frontend'
]

def should_reclassify(task_name, description):
    """Check if task should be moved out of Features category"""
    combined = f"{task_name} {description}".lower()
    for keyword in NON_FEATURE_KEYWORDS:
        if keyword in combined:
            return True
    return False

def reclassify_tasks():
    encoding = 'utf-16'
    rows = []
    fieldnames = []
    
    # Read the file
    try:
        with open(INPUT_FILE, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            print(f"Columns found: {fieldnames}\n")
            
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Analyze and update
    updated = 0
    for row in rows:
        name = row.get('Name', '')
        description = row.get('Description', '')
        
        # Check if this looks like a UI/Login/Registration task
        if should_reclassify(name, description):
            # Change category from "Feature Development" to "Implementation"
            for key in row:
                if key and ('categor' in key.lower() or 'phase' in key.lower() or 'type' in key.lower()):
                    old_value = row[key]
                    if 'feature' in old_value.lower():
                        row[key] = 'Implementation & Setup'
                        print(f"✓ Reclassified: {name[:50]}... from '{old_value}' to 'Implementation & Setup'")
                        updated += 1
                        break
    
    # Write back
    try:
        with open(OUTPUT_FILE, 'w', encoding=encoding, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"\n✓ Successfully updated {updated} tasks")
        print(f"✓ CSV saved to: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    reclassify_tasks()
