import os
import re

root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Update main containers to be wider on large screens
    content = re.sub(r'max-w-lg\s+mx-auto', r'max-w-5xl mx-auto w-full transition-all duration-300', content)
    content = re.sub(r'max-w-2xl\s+mx-auto', r'max-w-5xl mx-auto w-full transition-all duration-300', content)
    content = re.sub(r'max-w-md\s+mx-auto', r'max-w-5xl mx-auto w-full transition-all duration-300', content)

    # 2. Make grids responsive
    # Services grid (4 items to 2 on small, 4 on medium, 8 on large if applicable)
    content = re.sub(r'grid\s+grid-cols-4\s+gap-gutter', r'grid grid-cols-2 sm:grid-cols-4 md:grid-cols-4 lg:grid-cols-8 gap-4 sm:gap-gutter', content)
    
    # 2 items grids (Tips, Stats) to stack on very small screens
    content = re.sub(r'grid\s+grid-cols-2\s+gap-gutter', r'grid grid-cols-1 sm:grid-cols-2 gap-gutter', content)
    content = re.sub(r'grid\s+grid-cols-2\s+gap-sm', r'grid grid-cols-1 sm:grid-cols-2 gap-sm', content)

    # 3. Flex cards (like Donut chart and upcoming schedule) responsive stacking
    content = re.sub(r'flex\s+items-center\s+justify-between\s+gap-gutter', r'flex flex-col sm:flex-row items-center justify-between gap-gutter text-center sm:text-left', content)
    
    # 4. For app cards (generic bento card style) make sure they have a nice hover effect
    # The bento cards usually have `bg-white dark:bg-slate-900 rounded-[32px] p-md shadow-...`
    # Let's just enhance any rounded-3xl or rounded-[32px] that has shadow
    content = re.sub(r'(rounded-3xl|rounded-\[32px\])\s+(p-md\s+shadow-[^ ]+)', r'\1 \2 hover:shadow-lg transition-shadow duration-300', content)

    # 5. Make hero images in cards responsive
    content = re.sub(r'h-48\s+object-cover', r'h-48 sm:h-64 md:h-80 object-cover', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated responsiveness in {filepath}")

for root, dirs, files in os.walk(root_dir):
    if 'build' in root or '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            process_html_file(filepath)
