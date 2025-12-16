import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:5000"

def verify_csrf_fix():
    print("Verifying CSRF Fixes...")
    
    try:
        # 1. Check Registration Page
        print("\nChecking Registration Page...")
        try:
            with urllib.request.urlopen(f"{BASE_URL}/register") as response:
                content = response.read().decode('utf-8')
                
                # Check for Meta Tag
                if '<meta name="csrf-token" content="' in content:
                    print("PASSED: CSRF Meta tag found.")
                else:
                    print("FAILED: CSRF Meta tag NOT found.")
                    
                # Check for script.js
                if 'src="/static/js/script.js"' in content:
                    print("PASSED: script.js inclusion found.")
                else:
                    print("FAILED: script.js inclusion NOT found.")
                    
                # Check for Form ID
                if 'id="registerForm"' in content:
                    print("PASSED: Registration form ID found.")
                else:
                    print("FAILED: Registration form ID NOT found.")

                # Check for Hidden CSRF Token
                if 'name="csrf_token"' in content:
                     print("PASSED: Hidden CSRF token input found.")
                else:
                     print("FAILED: Hidden CSRF token input NOT found.")
                     
        except urllib.error.URLError as e:
            print(f"FAILED: Could not connect to server. {e}")
            print("Please ensure the Flask application is running.")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    verify_csrf_fix()
