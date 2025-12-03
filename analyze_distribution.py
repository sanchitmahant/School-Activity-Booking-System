import csv
from collections import defaultdict

INPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'

def analyze_distribution():
    encoding = 'utf-16'
    try:
        with open(INPUT_FILE, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            
            # Count tasks per assignee
            task_counts = defaultdict(list)
            all_rows = list(reader)
            
            for i, row in enumerate(all_rows, 1):
                assignee = row.get('Assignee', '').strip()
                task_name = row.get('Name', '').strip()
                if assignee:
                    task_counts[assignee].append((i, task_name))
            
            print("=" * 100)
            print("CURRENT TASK DISTRIBUTION")
            print("=" * 100)
            
            total_tasks = sum(len(tasks) for tasks in task_counts.values())
            num_members = len(task_counts)
            ideal_per_member = total_tasks / num_members
            
            for assignee in sorted(task_counts.keys()):
                tasks = task_counts[assignee]
                print(f"\n{assignee}: {len(tasks)} tasks")
                for row_num, task_name in tasks:
                    print(f"  Row {row_num}: {task_name}")
            
            print(f"\n{'-' * 100}")
            print(f"Total tasks: {total_tasks}")
            print(f"Team members: {num_members}")
            print(f"Ideal tasks per member: {ideal_per_member:.2f}")
            print(f"Target distribution: {int(ideal_per_member)} or {int(ideal_per_member) + 1} tasks each")
            
            # Suggest redistribution
            print(f"\n{'=' * 100}")
            print("SUGGESTED REDISTRIBUTION")
            print("=" * 100)
            print(f"To achieve equal distribution with {total_tasks} tasks among {num_members} members:")
            
            base_tasks = total_tasks // num_members
            extra_tasks = total_tasks % num_members
            
            print(f"  - {num_members - extra_tasks} members should have {base_tasks} tasks")
            print(f"  - {extra_tasks} members should have {base_tasks + 1} tasks")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_distribution()
