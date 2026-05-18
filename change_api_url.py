import os
import sys

if len(sys.argv) < 2:
    print("Usage: python change_api_url.py <new_url>")
    print("Example: python change_api_url.py https://abc1-23-45.ngrok-free.app")
    sys.exit(1)

new_url = sys.argv[1].rstrip('/')
current_url = "http://10.200.54.163:3000"
root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

# Find current URL in one of the files if it changed from above
def find_current_url():
    target_file = os.path.join(root_dir, "scan.html")
    if os.path.exists(target_file):
        with open(target_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        import re
        match = re.search(r'const apiBase = window\.ECOCYCLE_API_BASE \|\| "(http[^"]+)";', content)
        if match:
            return match.group(1)
    return current_url

detected_current_url = find_current_url()
print(f"Replacing {detected_current_url} with {new_url}...")

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if detected_current_url in content:
            updated = content.replace(detected_current_url, new_url)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated)
            print(f"Updated URL in {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

for root, dirs, files in os.walk(root_dir):
    if 'node_modules' in root or '.git' in root or 'build' in root:
        continue
    for file in files:
        if file.endswith(('.html', '.js', '.json', '.xml', '.java', '.kt')):
            process_file(os.path.join(root, file))

print("Successfully updated all URLs! Please rebuild the Android app to sync the assets folder.")
