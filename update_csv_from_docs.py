import csv
import os

INPUT_CSV = 'documentation/Project_Plan_Updated_2025.csv'
OUTPUT_CSV = 'documentation/Project_Plan_Updated_2025.csv'

# Assignments derived from restored documentation to ensure alignment
ASSIGNMENTS = {
    "Phase 1: Inception & Scoping": "Sanchit Kaushal",
    "Requirements Engineering": "Mohd Sharjeel",
    "Phase 2: Architecture & Database Design": "Shiva Kasula",
    "Database Schema Design (3NF)": "Shiva Kasula",
    "Security Architecture": "Sanchit Kaushal",
    "UI/UX Design System": "Mohd Sharjeel",
    "Phase 3: Core Authentication System": "Sanchit Kaushal",
    "Role-Based Access Control (RBAC)": "Sanchit Kaushal",
    "Parent Portal Development": "Mohd Sharjeel",
    "Phase 4: Advanced Booking Engine": "Shiva Kasula",
    "Database Transaction Management": "Shiva Kasula",
    "Waitlist System (Automated)": "Shiva Kasula",
    "Payment Flow Implementation": "Shiva Kasula",
    "Phase 5: Advanced Features Integration": "Chichebendu Blessed Umeh",
    "Email Notification System": "Chichebendu Blessed Umeh",
    "Calendar Integration (.ics Files)": "Chichebendu Blessed Umeh",
    "PDF Invoice Generation": "Chichebendu Blessed Umeh",
    "Admin Portal Development": "Sanchit Kaushal",
    "Tutor Portal Development": "Chichebendu Blessed Umeh",
    "≡ƒåò Tutor Registration & Approval System": "Chichebendu Blessed Umeh",
    "Phase 6: Deployment Preparation": "Sanchit Kaushal",
    "Testing & Quality Assurance": "Mohd Sharjeel",
    "Documentation & Academic Compliance": "Mohd Sharjeel"
}

def update_csv():
    rows = []
    with open(INPUT_CSV, 'r', encoding='utf-16') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            task_name = row['Name']
            # Update Assignee if mapped
            if task_name in ASSIGNMENTS:
                row['Assignee'] = ASSIGNMENTS[task_name]
            rows.append(row)
            
    with open(OUTPUT_CSV, 'w', encoding='utf-16', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Updated {len(rows)} tasks in {OUTPUT_CSV}")
    
    # Verify counts
    counts = {}
    for row in rows:
        assignee = row['Assignee']
        counts[assignee] = counts.get(assignee, 0) + 1
        
    print("\nNew Distribution:")
    for assignee, count in counts.items():
        print(f"{assignee}: {count}")

if __name__ == "__main__":
    update_csv()
