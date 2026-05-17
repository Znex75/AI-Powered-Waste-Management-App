import os
import re

root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

# The header to remove from the untracked files
bad_header_pattern = re.compile(r'<header class="bg-background docked full-width top-0 sticky z-50">.*?</header>', re.DOTALL)

nav_template = """<!-- BottomNavBar -->
<button class="mobile-fab fixed right-6 w-14 h-14 bg-primary text-on-primary rounded-2xl shadow-[0_8px_24px_rgba(0,107,95,0.4)] flex items-center justify-center active:scale-90 transition-transform z-40">
<span class="material-symbols-outlined text-[32px]" data-icon="add">add</span>
</button>
<nav class="mobile-bottom-nav fixed bottom-0 left-0 w-full z-50 flex justify-around items-center bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-t border-slate-100 dark:border-slate-800 shadow-[0_-4px_12px_rgba(45,212,191,0.08)]">
<a class="flex flex-col items-center justify-center text-teal-600 dark:text-teal-400 bg-teal-50 dark:bg-teal-900/20 rounded-2xl px-4 py-2 active:scale-90 transition-all duration-300 ease-out" href="{prefix}dashboard.html">
<span class="material-symbols-outlined" data-icon="home">home</span>
<span class="font-plus-jakarta-sans text-[11px] font-semibold">Home</span>
</a>
<a class="flex flex-col items-center justify-center text-slate-400 dark:text-slate-500 px-4 py-2 hover:text-teal-500 dark:hover:text-teal-300 transition-colors active:scale-90 transition-all duration-300 ease-out" href="{prefix}scan.html">
<span class="material-symbols-outlined mb-1">center_focus_weak</span>
<span class="font-plus-jakarta text-[11px] font-medium">Scanner</span>
</a>
<a class="flex flex-col items-center justify-center text-slate-400 dark:text-slate-500 px-4 py-2 hover:text-teal-500 dark:hover:text-teal-300 transition-colors active:scale-90 transition-all duration-300 ease-out" href="{prefix}marketPlace.html">
<span class="material-symbols-outlined" data-icon="storefront" style="font-variation-settings: 'FILL' 1;">storefront</span>
<span class="font-plus-jakarta-sans text-[11px] font-semibold">Market</span>
</a>
<a class="flex flex-col items-center justify-center text-slate-400 dark:text-slate-500 px-4 py-1 hover:text-teal-500 dark:hover:text-teal-300 active:scale-90 transition-transform duration-150" href="{prefix}Authentication/user.html">
<span class="material-symbols-outlined" data-icon="person">person</span>
<span class="font-plus-jakarta-sans text-[11px] font-semibold">Profile</span>
</a>
</nav>"""

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # Remove the bad header if it exists (from untracked files)
    content = bad_header_pattern.sub('', content)

    # Determine prefix
    if 'android\\app\\src\\main\\assets' in filepath:
        rel_path = os.path.relpath(filepath, os.path.join(root_dir, 'android', 'app', 'src', 'main', 'assets'))
    else:
        rel_path = os.path.relpath(filepath, root_dir)
        
    depth = rel_path.count(os.sep)
    prefix = "../" * depth

    new_nav = nav_template.replace('{prefix}', prefix)

    # Regex to find existing BottomNavBar and replace it
    # We will look for <button class="mobile-fab... up to </nav>
    # Or <!-- BottomNavBar --> ... </nav>
    
    bottom_nav_pattern = re.compile(r'<!--\s*BottomNavBar\s*-->.*?</nav>', re.DOTALL)
    alt_bottom_nav_pattern = re.compile(r'<button class="mobile-fab[^>]*>.*?</nav>', re.DOTALL)
    
    if bottom_nav_pattern.search(content):
        content = bottom_nav_pattern.sub(new_nav, content)
    elif alt_bottom_nav_pattern.search(content):
        content = alt_bottom_nav_pattern.sub(new_nav, content)
    else:
        # If it doesn't exist, insert before </body>
        body_end_pattern = re.compile(r'</body>', re.IGNORECASE)
        match = body_end_pattern.search(content)
        if match:
            content = content[:match.start()] + '\n' + new_nav + '\n' + content[match.start():]
        else:
            print(f"Warning: No </body> tag found in {filepath}")
            # Just append to the end
            content = content + '\n' + new_nav

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk(root_dir):
    if 'build' in root or '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            process_html_file(filepath)
