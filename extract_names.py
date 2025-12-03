import csv

def try_read(encoding):
    try:
        with open('documentation/Project_Plan_Updated_2025.csv', 'r', encoding=encoding) as f:
            # csv module doesn't handle null bytes well if they are part of the encoding but read as ascii
            # so we read lines first
            lines = [line.replace('\0', '') for line in f.readlines()]
            # Actually, for utf-16, we should just let python handle it.
            # But if it failed before, maybe it's because I didn't specify utf-16.
            pass

        with open('documentation/Project_Plan_Updated_2025.csv', 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            print(f"Successfully read with {encoding}")
            print(f"Columns: {reader.fieldnames}")
            assigned_to = set()
            for row in reader:
                for key in row:
                    if key and 'assign' in key.lower():
                        if row[key]:
                            assigned_to.add(row[key])
            return assigned_to
    except Exception as e:
        print(f"Failed with {encoding}: {e}")
        return None

names = try_read('utf-16')
if names is None:
    names = try_read('utf-16le')

if names:
    print("\nFound Names:")
    for name in names:
        print(name)
else:
    print("Could not read file with any encoding.")
