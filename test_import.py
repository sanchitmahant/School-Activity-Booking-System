import sys
import os

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

try:
    import app
    print("Successfully imported app module")
    if hasattr(app, 'app'):
        print("Found 'app' object in app module")
    else:
        print("Did NOT find 'app' object in app module")
        print(f"Dir(app): {dir(app)}")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
