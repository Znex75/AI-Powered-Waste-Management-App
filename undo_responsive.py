import os
import re

root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Revert container width
    if "user.html" in filepath:
        content = content.replace("max-w-5xl mx-auto w-full transition-all duration-300", "max-w-2xl mx-auto")
    elif any(name in filepath for name in ["signIn.html", "signUp.html", "forgotPassword.html", "resetPassword.html"]):
        content = content.replace("max-w-5xl mx-auto w-full transition-all duration-300", "max-w-md mx-auto")
    else:
        content = content.replace("max-w-5xl mx-auto w-full transition-all duration-300", "max-w-lg mx-auto")

    # 2. Revert grids
    content = content.replace("grid grid-cols-2 sm:grid-cols-4 md:grid-cols-4 lg:grid-cols-8 gap-4 sm:gap-gutter", "grid grid-cols-4 gap-gutter")
    content = content.replace("grid grid-cols-1 sm:grid-cols-2 gap-gutter", "grid grid-cols-2 gap-gutter")
    content = content.replace("grid grid-cols-1 sm:grid-cols-2 gap-sm", "grid grid-cols-2 gap-sm")

    # 3. Revert flex cards
    content = content.replace("flex flex-col sm:flex-row items-center justify-between gap-gutter text-center sm:text-left", "flex items-center justify-between gap-gutter")

    # 4. Revert hover shadows
    content = content.replace(" hover:shadow-lg transition-shadow duration-300", "")

    # 5. Revert hero images
    content = content.replace("h-48 sm:h-64 md:h-80 object-cover", "h-48 object-cover")

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Reverted responsiveness in {filepath}")

for root, dirs, files in os.walk(root_dir):
    if 'build' in root or '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            process_html_file(filepath)
