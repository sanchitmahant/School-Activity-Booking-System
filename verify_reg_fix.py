import urllib.request
import urllib.parse
import urllib.error
import re
import random

BASE_URL = "http://127.0.0.1:5000"

def verify_registration_fix():
    print("Verifying Registration Fix...")
    
    rand_id = random.randint(1000, 9999)
    email = f"test_fix_{rand_id}@example.com"
    
    try:
        # 1. Get CSRF Token
        print("Fetching CSRF token...")
        with urllib.request.urlopen(f"{BASE_URL}/register") as response:
            content = response.read().decode('utf-8')
            cookie = response.headers.get('Set-Cookie')
            
            match = re.search(r'name="csrf_token" value="([^"]+)"', content)
            if not match:
                print("FAILED: Could not find CSRF token")
                return
            csrf_token = match.group(1)
            print("Got CSRF token.")

        # 2. Submit Form
        print(f"Submitting registration for {email}...")
        data = urllib.parse.urlencode({
            'csrf_token': csrf_token,
            'full_name': 'Test User',
            'email': email,
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'password123'
        }).encode('utf-8')
        
        req = urllib.request.Request(f"{BASE_URL}/register", data=data, method='POST')
        if cookie:
            req.add_header('Cookie', cookie)
            
        try:
            with urllib.request.urlopen(req) as post_response:
                # If we get here, it means 200 OK (or other success). 
                # Flask redirect usually returns 200 if it follows redirect automatically, 
                # or we check the final URL.
                final_url = post_response.geturl()
                print(f"Final URL: {final_url}")
                
                if "/login" in final_url:
                    print("PASSED: Redirected to login page.")
                elif "All fields are required" in post_response.read().decode('utf-8'):
                    print("FAILED: Still getting 'All fields are required' error")
                else:
                    print("NOTE: Check Final URL to confirm success.")
                    
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
            print(e.read().decode('utf-8'))

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    verify_registration_fix()
