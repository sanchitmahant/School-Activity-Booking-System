import sqlite3

def check_schema():
    try:
        conn = sqlite3.connect('instance/booking_system_v2.db')
        cursor = conn.cursor()
        
        print("Tables in DB:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(table[0])
            
        print("\nChecking 'booking' table schema:")
        cursor.execute("PRAGMA table_info(booking)")
        columns = cursor.fetchall()
        
        found_created_at = False
        for col in columns:
            print(col)
            if col[1] == 'created_at':
                found_created_at = True
                
        if found_created_at:
            print("\nSUCCESS: 'created_at' column found.")
        else:
            print("\nFAILURE: 'created_at' column NOT found.")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_schema()
