import os
import re

root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

dark_mode_snippet = """
    // Apply dark mode theme if saved
    const isDark = localStorage.getItem('theme') === 'dark';
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
"""

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    if "Apply dark mode theme if saved" not in content and "Error fetching user for drawer" in content:
        # Insert the snippet right after the closing brace of the try/catch inside DOMContentLoaded
        # Specifically, we look for: console.error("Error fetching user for drawer:", err); }
        content = re.sub(
            r'(console\.error\("Error fetching user for drawer:", err\);\s*\})',
            r'\1\n' + dark_mode_snippet,
            content,
            count=1
        )
            
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added dark mode init to {filepath}")

for root, dirs, files in os.walk(root_dir):
    if 'build' in root or '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            process_html_file(filepath)
