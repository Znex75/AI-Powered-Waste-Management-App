import os
import re

root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

# Define the new drawer content block to replace the existing one
drawer_content_template = """<div class="p-4 flex flex-col gap-2 flex-1">
<a href="{prefix}dashboard.html" class="flex items-center gap-4 px-4 py-3 bg-[#4caf50] text-white rounded-xl">
<span class="material-symbols-outlined">home</span>
<span class="font-semibold flex-1">Homepage</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}scan.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">center_focus_weak</span>
<span class="font-semibold flex-1">Scanner</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}marketPlace.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">storefront</span>
<span class="font-semibold flex-1">Market</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}Authentication/user.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">person</span>
<span class="font-semibold flex-1">Profile</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}schedule.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">calendar_today</span>
<span class="font-semibold flex-1">Schedule</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}recycle.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">recycling</span>
<span class="font-semibold flex-1">Recycle</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}events.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">event</span>
<span class="font-semibold flex-1">Events</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}tips.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">lightbulb</span>
<span class="font-semibold flex-1">Tips</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}blog.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">article</span>
<span class="font-semibold flex-1">Blog</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}donate.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">volunteer_activism</span>
<span class="font-semibold flex-1">Donate</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}community.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">groups</span>
<span class="font-semibold flex-1">Community</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}reports.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">pie_chart</span>
<span class="font-semibold flex-1">Reports</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
</div>"""

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    if 'android\\app\\src\\main\\assets' in filepath:
        rel_path = os.path.relpath(filepath, os.path.join(root_dir, 'android', 'app', 'src', 'main', 'assets'))
    else:
        rel_path = os.path.relpath(filepath, root_dir)
        
    depth = rel_path.count(os.sep)
    prefix = "../" * depth

    # Regex to find the <div class="p-4 flex flex-col gap-2 flex-1"> block inside the drawer
    # and replace it.
    drawer_pattern = re.compile(r'<div class="p-4 flex flex-col gap-2 flex-1">.*?</div>\s*<div class="p-4 border-t border-slate-100">', re.DOTALL)
    
    new_drawer_content = drawer_content_template.replace('{prefix}', prefix) + '\n<div class="p-4 border-t border-slate-100">'
    
    if drawer_pattern.search(content):
        content = drawer_pattern.sub(new_drawer_content, content, count=1)
            
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated drawer links in {filepath}")

for root, dirs, files in os.walk(root_dir):
    if 'build' in root or '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            process_html_file(filepath)
