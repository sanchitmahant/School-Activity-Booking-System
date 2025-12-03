import csv
import sys

TEAM_MEMBERS = [
    "Sanchit Kaushal",
    "Mohd Sharjeel",
    "Chichebendu Blessed Umeh",
    "Shiva Kasula"
]

INPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'
OUTPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'

def redistribute_tasks():
    rows = []
    fieldnames = []
    encoding = 'utf-16'

    # Read the file
    try:
        with open(INPUT_FILE, 'r', encoding=encoding) as f:
            # Handle potential BOM or null bytes if needed, but csv module usually handles it with correct encoding
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print(f"Total tasks found: {len(rows)}")

    # Redistribute
    member_idx = 0
    updated_rows = []
    
    for row in rows:
        # Find the key for 'Assigned To'
        assign_key = None
        for key in row:
            if key and 'assign' in key.lower():
                assign_key = key
                break
        
        if assign_key:
            # Assign to next member
            row[assign_key] = TEAM_MEMBERS[member_idx]
            member_idx = (member_idx + 1) % len(TEAM_MEMBERS)
        
        updated_rows.append(row)

    # Write back
    try:
        with open(OUTPUT_FILE, 'w', encoding=encoding, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)
        print("Successfully redistributed tasks.")
        
        # Verify counts
        counts = {m: 0 for m in TEAM_MEMBERS}
        for row in updated_rows:
             for key in row:
                if key and 'assign' in key.lower():
                    name = row[key]
                    if name in counts:
                        counts[name] += 1
        
        print("\nTask Distribution:")
        for name, count in counts.items():
            print(f"{name}: {count}")

    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    redistribute_tasks()
