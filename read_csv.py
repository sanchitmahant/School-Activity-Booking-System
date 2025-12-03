import csv

INPUT_FILE = 'documentation/Project_Plan_Updated_2025.csv'

def read_tasks():
    encoding = 'utf-16'
    try:
        with open(INPUT_FILE, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            print(f"Columns: {reader.fieldnames}")
            for row in reader:
                print(row)
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    read_tasks()
