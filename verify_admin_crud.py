import urllib.request
import urllib.parse
import http.cookiejar
import re

BASE_URL = "http://127.0.0.1:5000"
ADMIN_EMAIL = "admin@school.edu"
ADMIN_PASSWORD = "admin123"

# Setup cookie jar
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]

def get_csrf_token(html):
    match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    if match:
        return match.group(1)
    return None

def login():
    print("Checking root route...")
    try:
        resp = opener.open(f"{BASE_URL}/")
        print(f"Root route status: {resp.getcode()}")
    except Exception as e:
        print(f"Root route failed: {e}")

    print("Logging in...")
    # Get Login Page for CSRF
    resp = opener.open(f"{BASE_URL}/admin/login")
    html = resp.read().decode('utf-8')
    csrf_token = get_csrf_token(html)
    
    if not csrf_token:
        print("Failed to get CSRF token")
        return None

    data = urllib.parse.urlencode({
        'email': ADMIN_EMAIL,
        'password': ADMIN_PASSWORD,
        'csrf_token': csrf_token
    }).encode('utf-8')
    
    resp = opener.open(f"{BASE_URL}/admin/login", data=data)
    html = resp.read().decode('utf-8')
    
    if "Command Center" in html:
        print("Login Successful")
        return csrf_token
    else:
        print("Login Failed")
        return None

def verify_crud():
    # We need a fresh CSRF token from the dashboard for subsequent requests
    resp = opener.open(f"{BASE_URL}/admin/dashboard")
    html = resp.read().decode('utf-8')
    csrf_token = get_csrf_token(html)

    # 1. Create Tutor
    print("\n--- Testing Tutor CRUD ---")
    tutor_data = urllib.parse.urlencode({
        'full_name': 'CRUD Test Tutor',
        'email': 'crudtutor@test.com',
        'password': 'password',
        'specialization': 'Testing',
        'csrf_token': csrf_token
    }).encode('utf-8')
    
    try:
        resp = opener.open(f"{BASE_URL}/admin/tutor/add", data=tutor_data)
        html = resp.read().decode('utf-8')
        if "Tutor added successfully" in html:
            print("Create Tutor: OK")
        else:
            print("Create Tutor: Failed (Message not found)")
    except Exception as e:
        print(f"Create Tutor: Failed ({e})")

    # Get Tutor ID
    resp = opener.open(f"{BASE_URL}/admin/dashboard")
    html = resp.read().decode('utf-8')
    
    # Regex to find the ID of the tutor we just added
    # Looking for data-id="..." ... CRUD Test Tutor
    # This is tricky with regex, let's try to find the name and look backwards or use a specific pattern
    # Pattern: data-id="(\d+)"[^>]*data-name="CRUD Test Tutor"
    match = re.search(r'data-id="(\d+)"[^>]*data-name="CRUD Test Tutor"', html)
    if not match:
        print("Could not find created tutor ID")
        return
    
    tutor_id = match.group(1)
    print(f"Tutor ID: {tutor_id}")

    # 2. Edit Tutor
    edit_data = urllib.parse.urlencode({
        'full_name': 'Updated CRUD Tutor',
        'email': 'crudtutor@test.com',
        'specialization': 'Advanced Testing',
        'csrf_token': csrf_token
    }).encode('utf-8')
    
    try:
        resp = opener.open(f"{BASE_URL}/admin/tutor/edit/{tutor_id}", data=edit_data)
        html = resp.read().decode('utf-8')
        if "Tutor updated successfully" in html:
            print("Edit Tutor: OK")
        else:
            print("Edit Tutor: Failed")
    except Exception as e:
        print(f"Edit Tutor: Failed ({e})")

    # 3. Create Activity
    print("\n--- Testing Activity CRUD ---")
    activity_data = urllib.parse.urlencode({
        'name': 'CRUD Activity',
        'price': '50.00',
        'day': 'Friday',
        'start': '14:00',
        'end': '15:00',
        'tutor_id': tutor_id,
        'csrf_token': csrf_token
    }).encode('utf-8')
    
    try:
        resp = opener.open(f"{BASE_URL}/admin/activity/add", data=activity_data)
        html = resp.read().decode('utf-8')
        if "Activity created successfully" in html:
            print("Create Activity: OK")
        else:
            print("Create Activity: Failed")
    except Exception as e:
        print(f"Create Activity: Failed ({e})")

    # Get Activity ID
    resp = opener.open(f"{BASE_URL}/admin/dashboard")
    html = resp.read().decode('utf-8')
    
    match = re.search(r'data-id="(\d+)"[^>]*data-name="CRUD Activity"', html)
    if not match:
        print("Could not find created activity ID")
        return
    
    activity_id = match.group(1)
    print(f"Activity ID: {activity_id}")

    # 4. Edit Activity
    edit_act_data = urllib.parse.urlencode({
        'name': 'Updated CRUD Activity',
        'price': '75.00',
        'day': 'Friday',
        'start': '14:00',
        'end': '16:00',
        'tutor_id': tutor_id,
        'csrf_token': csrf_token
    }).encode('utf-8')
    
    try:
        resp = opener.open(f"{BASE_URL}/admin/activity/edit/{activity_id}", data=edit_act_data)
        html = resp.read().decode('utf-8')
        if "Activity updated successfully" in html:
            print("Edit Activity: OK")
        else:
            print("Edit Activity: Failed")
    except Exception as e:
        print(f"Edit Activity: Failed ({e})")

    # 5. Delete Activity
    print("\n--- Testing Deletion ---")
    del_act_data = urllib.parse.urlencode({'csrf_token': csrf_token}).encode('utf-8')
    try:
        resp = opener.open(f"{BASE_URL}/admin/activity/delete/{activity_id}", data=del_act_data)
        html = resp.read().decode('utf-8')
        if "Activity deleted successfully" in html:
            print("Delete Activity: OK")
        else:
            print("Delete Activity: Failed")
    except Exception as e:
        print(f"Delete Activity: Failed ({e})")

    # 6. Delete Tutor
    del_tutor_data = urllib.parse.urlencode({'csrf_token': csrf_token}).encode('utf-8')
    try:
        resp = opener.open(f"{BASE_URL}/admin/tutor/delete/{tutor_id}", data=del_tutor_data)
        html = resp.read().decode('utf-8')
        if "Tutor deleted successfully" in html:
            print("Delete Tutor: OK")
        else:
            print("Delete Tutor: Failed")
    except Exception as e:
        print(f"Delete Tutor: Failed ({e})")

if __name__ == "__main__":
    try:
        if login():
            verify_crud()
    except Exception as e:
        print(f"An error occurred: {e}")
        if hasattr(e, 'read'):
            print(e.read().decode('utf-8'))
