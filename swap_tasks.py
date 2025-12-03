import csv
import os

INPUT_CSV = 'documentation/Project_Plan_Updated_2025.csv'
OUTPUT_CSV = 'documentation/Project_Plan_Updated_2025.csv'

# New Assignments
ASSIGNMENTS = {
    # Sanchit (Takes Blessed's tasks)
    "Phase 5: Advanced Features Integration": "Sanchit Kaushal",
    "Email Notification System": "Sanchit Kaushal",
    "Calendar Integration (.ics Files)": "Sanchit Kaushal",
    "PDF Invoice Generation": "Sanchit Kaushal",
    "Tutor Portal Development": "Sanchit Kaushal",
    "≡ƒåò Tutor Registration & Approval System": "Sanchit Kaushal",
    
    # Chichebendu (Takes Sanchit's tasks)
    "Phase 1: Inception & Scoping": "Chichebendu Blessed Umeh",
    "Security Architecture": "Chichebendu Blessed Umeh",
    "Phase 3: Core Authentication System": "Chichebendu Blessed Umeh",
    "Role-Based Access Control (RBAC)": "Chichebendu Blessed Umeh",
    "Admin Portal Development": "Chichebendu Blessed Umeh",
    "Phase 6: Deployment Preparation": "Chichebendu Blessed Umeh",
    
    # Sharjeel (Keeps his, but UI/UX replaced)
    "Requirements Engineering": "Mohd Sharjeel",
    "Parent Portal Development": "Mohd Sharjeel",
    "Testing & Quality Assurance": "Mohd Sharjeel",
    "Documentation & Academic Compliance": "Mohd Sharjeel",
    # UI/UX replaced below
}

def update_csv():
    rows = []
    with open(INPUT_CSV, 'r', encoding='utf-16') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            task_name = row['Name']
            
            # Replace UI/UX with Attendance System (Assigned to Sharjeel)
            if task_name == "UI/UX Design System":
                row['Name'] = "Attendance System Implementation"
                row['Description'] = "Backend logic for tracking student attendance, status updates, and reporting."
                row['Detailed Presentation Script (Read this for Viva/Questions)'] = "Implemented a robust attendance tracking system allowing tutors to mark students as Present, Late, or Absent. The system updates the database in real-time and provides summary reports for administrators. It uses a relational model linking Bookings to Attendance records."
                row['Assignee'] = "Mohd Sharjeel"
            
            # Update Assignee if mapped
            elif task_name in ASSIGNMENTS:
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
