import subprocess
import requests
import time
import re
import os

# 💡 Change these paths to match your system
NGROK_PATH = r"C:\Users\pranali\Downloads\ngrok-v3-stable-windows-amd64\ngrok.exe"
FLUTTER_API_FILE = r"D:\HeartRiskApp\mobile_app\lib\services\api_service.dart"

def start_ngrok():
    # Kill any previous ngrok instance
    subprocess.run("taskkill /F /IM ngrok.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Start ngrok in background
    subprocess.Popen([NGROK_PATH, "http", "5000"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print("🚀 Starting ngrok tunnel...")
    time.sleep(3)  # brief wait before checking

def get_ngrok_url(max_retries=10, delay=2):
    """Try fetching ngrok tunnel URL multiple times until it appears."""
    for attempt in range(max_retries):
        try:
            res = requests.get("http://127.0.0.1:4040/api/tunnels")
            data = res.json()
            tunnels = data.get("tunnels", [])
            
            if tunnels:
                url = tunnels[0]["public_url"]
                print(f"✅ Ngrok tunnel established: {url}")
                return url
            else:
                print(f"⏳ Waiting for ngrok tunnel... (Attempt {attempt+1}/{max_retries})")
        except Exception as e:
            print(f"⚠️ Error accessing ngrok API (Attempt {attempt+1}): {e}")
        
        time.sleep(delay)

    print("❌ Ngrok tunnel not found after several attempts.")
    return None

def update_flutter_url(new_url):
    if not os.path.exists(FLUTTER_API_FILE):
        print(f"❌ Flutter file not found: {FLUTTER_API_FILE}")
        return
    
    with open(FLUTTER_API_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    updated_content = re.sub(
        r'const String baseUrl = ".*?";',
        f'const String baseUrl = "{new_url}";',
        content
    )
    
    with open(FLUTTER_API_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print("✅ Flutter baseUrl updated successfully!")

if __name__ == "__main__":
    start_ngrok()
    new_url = get_ngrok_url()
    if new_url:
        update_flutter_url(new_url)
        print("\n🎯 All done! Your Flutter app now uses the new ngrok URL.")
        print("👉 You can now run:  flutter run")
    else:
        print("❌ Could not retrieve ngrok URL. Please check your ngrok setup.")
