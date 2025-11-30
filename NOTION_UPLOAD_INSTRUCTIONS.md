# How to Upload Project Plan to Notion

## Step 1: Install Python Library
```bash
pip install requests
```

## Step 2: Get Notion Integration Token

1. Go to: https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. Name: `Project Plan Uploader`
4. Select your workspace
5. Click **"Submit"**
6. Copy the **"Internal Integration Token"** (starts with `secret_...`)

## Step 3: Create Database in Notion

1. Open Notion
2. Create a new page for your project
3. Type `/database` and select **"Table - Inline"**
4. Name it: `Project Plan`

## Step 4: Get Database ID

1. Open your new database in Notion
2. Click the **"..."** menu (top right)
3. Click **"Copy link"**
4. The URL looks like: `https://www.notion.so/xxxxx?v=yyyyy`
5. Copy only the `xxxxx` part (the long string before `?v=`)

## Step 5: Share Database with Integration

⚠️ **CRITICAL STEP** - Don't skip this!

1. Open your database in Notion
2. Click the **"..."** menu (top right)
3. Click **"Connections"**
4. Click **"Add connections"**
5. Select **"Project Plan Uploader"**

## Step 6: Configure the Script

1. Open `upload_to_notion.py`
2. Replace `YOUR_NOTION_TOKEN_HERE` with your token from Step 2
3. Replace `YOUR_DATABASE_ID_HERE` with your ID from Step 4
4. Save the file

## Step 7: Run the Script

```bash
python upload_to_notion.py
```

You should see:
```
✅ Database found! Now adding properties...
✅ Database schema updated!
📄 Found 50 tasks to upload...
✅ [1/50] Technology Selection
✅ [2/50] Repository Initialization
...
🎉 Done! Successfully uploaded 50/50 tasks.
```

## Step 8: View in Notion

Go to your Notion database and you'll see all 50 tasks organized beautifully!

---

## Troubleshooting

**Error: "Invalid token"**
- Make sure you copied the entire token (starts with `secret_`)
- Check there are no extra spaces

**Error: "Database not found"**
- Make sure you copied the correct Database ID
- Make sure you completed Step 5 (sharing the database)

**Error: "Forbidden"**
- You didn't share the database with the integration (Step 5)
- Go back and complete Step 5

---

## What Gets Uploaded

The script creates these columns in Notion:
- **Task** (Title)
- **Phase** (Select)
- **Assigned To** (Select - Sanchit/Chichebendu/Shiva/Sharjeel)
- **Start Date** (Date)
- **End Date** (Date)
- **Status** (Select - Complete)
- **Description** (Text)
- **Technical Details** (Text)

All 50 tasks from `Project_Plan.csv` will be imported!
