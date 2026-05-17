import os
import re

root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

def process_html_file(filepath):
    # Skip notifications.html itself
    if "notifications.html" in filepath:
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Determine prefix based on depth from root
    if 'android\\app\\src\\main\\assets' in filepath:
        rel_path = os.path.relpath(filepath, os.path.join(root_dir, 'android', 'app', 'src', 'main', 'assets'))
    else:
        rel_path = os.path.relpath(filepath, root_dir)
        
    depth = rel_path.count(os.sep)
    prefix = "../" * depth

    # Target button element
    target_btn = 'aria-label="Notifications"'
    
    # We want to replace `<button ... aria-label="Notifications">` with `<button onclick="location.href='{prefix}notifications.html'" ...>`
    # Let's use regex to find and replace it if it doesn't already have onclick
    pattern = re.compile(r'<button([^>]*aria-label="Notifications"[^>]*)>', re.IGNORECASE)
    
    def replacement(match):
        attrs = match.group(1)
        if 'onclick' in attrs:
            # Already has onclick, let's update it or leave it
            return match.group(0)
        return f'<button onclick="location.href=\'{prefix}notifications.html\'"{attrs}>'

    content = pattern.sub(replacement, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Linked notifications in {filepath}")

for root, dirs, files in os.walk(root_dir):
    if 'build' in root or '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            process_html_file(filepath)
