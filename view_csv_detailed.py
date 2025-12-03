import csv

INPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'

def read_tasks():
    encoding = 'utf-16'
    try:
        with open(INPUT_FILE, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            print(f"Columns: {fieldnames}")
            print(f"\n{'='*100}\n")
            
            all_rows = list(reader)
            print(f"Total rows: {len(all_rows)}")
            
            # Print first 15 rows
            print(f"\nFirst 15 rows:")
            print('-' * 100)
            for i, row in enumerate(all_rows[:15]):
                print(f"\nRow {i+1}:")
                for key, value in row.items():
                    if value:  # Only print non-empty values
                        print(f"  {key}: {value}")
            
            # Check for Category column
            if 'Category' in fieldnames:
                categories = {}
                for row in all_rows:
                    cat = row.get('Category', '').strip()
                    if cat:
                        categories[cat] = categories.get(cat, 0) + 1
                
                print(f"\n\n{'='*100}")
                print("CATEGORY DISTRIBUTION:")
                print('='*100)
                for cat, count in sorted(categories.items()):
                    print(f"{cat}: {count} tasks")
            
            # Save full content to file
            with open('csv_full_content.txt', 'w', encoding='utf-8') as out:
                out.write(f"Columns: {fieldnames}\n\n")
                out.write(f"Total rows: {len(all_rows)}\n\n")
                out.write('='*100 + '\n')
                
                for i, row in enumerate(all_rows):
                    out.write(f"\n--- Row {i+1} ---\n")
                    for key, value in row.items():
                        if value:
                            out.write(f"{key}: {value}\n")
            
            print(f"\n\nFull content saved to csv_full_content.txt")
            
    except Exception as e:
        print(f"Error reading file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    read_tasks()
