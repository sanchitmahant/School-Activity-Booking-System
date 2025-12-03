import pandas as pd

# Read the CSV file
csv_path = r'documentation\Project_Plan_Updated_2025.csv'
df = pd.read_csv(csv_path)

# Display basic information
print(f"Total rows: {len(df)}")
print(f"\nColumn names: {list(df.columns)}")
print(f"\nFirst 10 rows:")
print(df.head(10).to_string())
print(f"\n\nLast 10 rows:")
print(df.tail(10).to_string())

# Check for categories if there's a Category column
if 'Category' in df.columns:
    print(f"\n\nUnique categories:")
    print(df['Category'].value_counts())

# Save to text file for easier viewing
with open('csv_preview.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total rows: {len(df)}\n")
    f.write(f"\nColumn names: {list(df.columns)}\n")
    f.write(f"\n{'='*80}\n")
    f.write(f"ALL DATA:\n")
    f.write(f"{'='*80}\n")
    f.write(df.to_string())
    
print("\nCSV preview saved to csv_preview.txt")
