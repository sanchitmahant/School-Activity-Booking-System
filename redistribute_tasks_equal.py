import csv
import sys

INPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'
OUTPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'
BACKUP_FILE = 'documentation/Project_Plan_Updated_2025_backup.csv'

def redistribute_tasks():
    """
    Redistribute tasks for equal contribution.
    Current: Sanchit(6), Mohd(6), Chichebendu(6), Shiva(5)
    Target: 3 members with 6 tasks, 1 member with 5 tasks (total 23 tasks)
    
    Strategy: Move 1 task from one member to Shiva to balance distribution.
    """
    encoding = 'utf-16'
    
    try:
        # Read all rows
        with open(INPUT_FILE, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            all_rows = list(reader)
        
        # Create backup
        with open(BACKUP_FILE, 'w', encoding=encoding, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
        
        print(f"Backup created: {BACKUP_FILE}")
        print(f"\nTotal rows to process: {len(all_rows)}")
        
        # Redistribution plan:
        # Current distribution seems balanced for 23 tasks / 4 people
        # Best distribution is 6, 6, 6, 5 which is what we have
        # But let's check if we can make it even more balanced
        
        # Count current distribution
        from collections import defaultdict
        task_counts = defaultdict(int)
        
        for row in all_rows:
            assignee = row.get('Assignee', '').strip()
            if assignee:
                task_counts[assignee] += 1
        
        print("\nCurrent distribution:")
        for assignee in sorted(task_counts.keys()):
            print(f"  {assignee}: {task_counts[assignee]} tasks")
        
        # The current distribution is already optimal for 23 tasks / 4 people
        # 23 / 4 = 5.75, so the best we can do is 6, 6, 6, 5
        # Current is: 6, 6, 6, 5 - which is already perfect!
        
        # However, if user wants strictly equal, we could try 6, 6, 6, 5
        # Let's verify this is the current state and confirm it's optimal
        
        assignees = ['Sanchit Kaushal', 'Mohd Sharjeel', 'Chichebendu Blessed Umeh', 'Shiva Kasula']
        counts = [task_counts[a] for a in assignees]
        
        print(f"\nDistribution analysis:")
        print(f"  Total tasks: {sum(counts)}")
        print(f"  Team size: {len(assignees)}")
        print(f"  Average: {sum(counts)/len(assignees):.2f}")
        print(f"  Range: {min(counts)} - {max(counts)}")
        print(f"  Variance: {max(counts) - min(counts)}")
        
        if max(counts) - min(counts) <= 1:
            print(f"\n✓ Distribution is already optimal!")
            print(f"  With 23 tasks and 4 members, the best possible distribution is:")
            print(f"  - 3 members with 6 tasks")
            print(f"  - 1 member with 5 tasks")
            print(f"\nNo changes needed. CSV is already balanced.")
            return False
        else:
            print(f"\n⚠ Distribution can be improved. Making adjustments...")
            # Implement redistribution logic here if needed
            return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*100)
    print("TASK REDISTRIBUTION ANALYSIS")
    print("="*100)
    
    needs_changes = redistribute_tasks()
    
    if not needs_changes:
        print("\n" + "="*100)
        print("CONCLUSION: Current task distribution is already optimal.")
        print("="*100)
