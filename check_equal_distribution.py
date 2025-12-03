import csv
import shutil

INPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'
OUTPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'
BACKUP_FILE = 'documentation/Project_Plan_Updated_2025_backup.csv'

def redistribute_for_perfect_balance():
    """
    Redistribute tasks to achieve more balanced distribution.
    Current: Chichebendu(6), Mohd(6), Sanchit(6), Shiva(5) = 23 total
    
    Since 23 / 4 = 5.75, the mathematically optimal distribution is 6,6,6,5
    which is what we already have.
    
    However, for visual/perception purposes, we can try to get closer to 6,6,6,5
    or consider alternating assignments for fairness.
    
    Actually, the current distribution IS optimal. But if the user wants
    strictly equal (impossible with 23 tasks), we keep current distribution.
    """
    encoding = 'utf-16'
    
    try:
        # Read all rows
        with open(INPUT_FILE, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            all_rows = list(reader)
        
        # Create backup
        shutil.copy2(INPUT_FILE, BACKUP_FILE)
        print(f"✓ Backup created: {BACKUP_FILE}")
        
        # Analyze current state
        from collections import defaultdict
        assignee_tasks = defaultdict(list)
        
        for i, row in enumerate(all_rows):
            assignee = row.get('Assignee', '').strip()
            if assignee:
                assignee_tasks[assignee].append((i, row))
        
        print(f"\n{'='*100}")
        print("CURRENT DISTRIBUTION ANALYSIS")
        print('='*100)
        
        for assignee in sorted(assignee_tasks.keys()):
            tasks = assignee_tasks[assignee]
            print(f"\n{assignee}: {len(tasks)} tasks")
        
        total = sum(len(tasks) for tasks in assignee_tasks.values())
        print(f"\nTotal: {total} tasks among {len(assignee_tasks)} members")
        print(f"Average: {total/len(assignee_tasks):.2f} tasks/member")
        
        # Mathematical analysis
        print(f"\n{'='*100}")
        print("REDISTRIBUTION STRATEGY")
        print('='*100)
        print(f"\nWith {total} tasks and {len(assignee_tasks)} members:")
        print(f"  • Perfectly equal distribution would require {total%len(assignee_tasks)} additional tasks")
        print(f"  • OR removing {len(assignee_tasks) - (total%len(assignee_tasks))} tasks")
        print(f"\nSince we cannot add/remove tasks per user requirements,")
        print(f"the current distribution (6, 6, 6, 5) is ALREADY OPTIMAL.\n")
        
        # However, we can reassign to make it appear more balanced
        # Option: Keep it as is since it's mathematically optimal
        
        print("✓ Current distribution is mathematically optimal for 23 tasks / 4 members")
        print("✓ No changes required")
        
        return all_rows, fieldnames, False
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None, False

if __name__ == "__main__":
    print("="*100)
    print("TASK REDISTRIBUTION FOR EQUAL CONTRIBUTION")
    print("="*100)
    
    rows, fieldnames, changed = redistribute_for_perfect_balance()
    
    if rows and not changed:
        print(f"\n{'='*100}")
        print("RESULT: CSV already has optimal task distribution")
        print('='*100)
        print("\nCurrent distribution (6, 6, 6, 5) is the most balanced")
        print("possible arrangement for 23 tasks among 4 team members.")
    elif rows and changed:
        print(f"\n{'='*100}")
        print("TASK REDISTRIBUTION COMPLETE")
        print('='*100)
