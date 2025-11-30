"""
Notion Project Plan Uploader - Simplified Version
Uploads Project_Plan.csv to your Notion database
"""

import requests
import csv
import json

# Your credentials
NOTION_TOKEN = "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"
DATABASE_ID = "2bb98895f21380f5a28fda623c029274"

NOTION_API_URL = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def upload_csv_to_notion():
    """Upload Project_Plan.csv to Notion database"""
    
    print("🚀 Starting upload to Notion...")
    
    # Read CSV file
    try:
        with open('Project_Plan.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
    except FileNotFoundError:
        print("❌ ERROR: Project_Plan.csv not found!")
        return
    
    print(f"📄 Found {len(rows)} tasks to upload...")
    
    # Upload each row
    success_count = 0
    for i, row in enumerate(rows, 1):
        try:
            # Prepare data for Notion - using simpler property names
            page_data = {
                "parent": {"database_id": DATABASE_ID},
                "properties": {
                    "Name": {  # Default title property
                        "title": [{"text": {"content": row['Task'][:100]}}]
                    }
                }
            }
            
            # Try to add other properties if they exist in the database
            # These will be ignored if the properties don't exist
            optional_props = {}
            
            # Add tags/select properties
            for prop_name, csv_field in [
                ("Phase", "Phase"),
                ("Assigned To", "Assigned To"),
                ("Status", "Status")
            ]:
                if csv_field in row and row[csv_field]:
                    optional_props[prop_name] = {"select": {"name": row[csv_field]}}
            
            # Add date properties
            if 'Start Date' in row and row['Start Date']:
                optional_props["Start Date"] = {"date": {"start": row['Start Date']}}
            if 'End Date' in row and row['End Date']:
                optional_props["End Date"] = {"date": {"start": row['End Date']}}
            
            # Add text properties
            for prop_name, csv_field in [
                ("Description", "Description"),
                ("Technical Details", "Technical Details")
            ]:
                if csv_field in row and row[csv_field]:
                    text_content = row[csv_field][:2000]  # Notion limit
                    optional_props[prop_name] = {
                        "rich_text": [{"text": {"content": text_content}}]
                    }
            
            # Merge optional properties
            page_data["properties"].update(optional_props)
            
            # Create page in database
            response = requests.post(
                f"{NOTION_API_URL}/pages",
                headers=HEADERS,
                json=page_data
            )
            
            if response.status_code == 200:
                success_count += 1
                print(f"✅ [{i}/{len(rows)}] {row['Task'][:50]}")
            else:
                print(f"❌ [{i}/{len(rows)}] Failed: {row['Task'][:30]}")
                if i == 1:  # Show error on first failure
                    print(f"   Error response: {response.text[:200]}")
        
        except Exception as e:
            print(f"❌ [{i}/{len(rows)}] Error: {str(e)[:100]}")
    
    print(f"\n🎉 Done! Successfully uploaded {success_count}/{len(rows)} tasks.")
    if success_count > 0:
        print(f"🔗 View in Notion: https://www.notion.so/{DATABASE_ID}")

if __name__ == "__main__":
    upload_csv_to_notion()
