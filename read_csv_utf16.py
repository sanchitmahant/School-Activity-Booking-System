import csv

INPUT_CSV = 'documentation/Project_Plan_Updated_2025.csv'

def read_csv():
    with open(INPUT_CSV, 'r', encoding='utf-16') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"Task: {row['Name']} | Assignee: {row['Assignee']}")

if __name__ == "__main__":
    read_csv()
