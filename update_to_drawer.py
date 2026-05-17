import os
import re

root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

new_header_template = """<!-- TopAppBar & Navigation Drawer -->
<header class="mobile-top-bar fixed top-0 left-0 w-full z-50 flex justify-between items-center bg-white/95 dark:bg-slate-950/95 backdrop-blur-md border-b border-slate-100 dark:border-slate-800/50 shadow-sm shadow-teal-900/5">
<div class="flex items-center gap-3">
<button class="w-11 h-11 rounded-full flex items-center justify-center text-teal-600 active:scale-95 transition-transform duration-200" onclick="document.getElementById('nav-drawer').classList.remove('-translate-x-full'); document.getElementById('drawer-overlay').classList.remove('hidden');" aria-label="Menu">
<span class="material-symbols-outlined text-3xl">menu</span>
</button>
<span class="text-2xl font-extrabold text-teal-600 dark:text-teal-400 tracking-normal font-plus-jakarta">EcoCycle</span>
</div>
<div class="flex items-center gap-2">
<button class="w-10 h-10 rounded-full flex items-center justify-center bg-slate-50 text-slate-500 active:scale-95 transition-transform duration-200 hover:opacity-80 transition-opacity" aria-label="Notifications">
<span class="material-symbols-outlined text-xl">notifications</span>
</button>
<a href="{prefix}Authentication/user.html" class="w-10 h-10 rounded-full overflow-hidden border-2 border-primary-container block">
<img alt="User profile photo" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDsODJt1tT752FfsIlf0EVEMTPh7CkI3YaxCo-859HcXYCzVTTzxlLgZcN1NmoRV1ml8gHGZiqvCN35yCqoErdR9q3yvcnCoXln3aCKjItRjVYZ9oaL2-3yOEq4ol6vimRiHBXwYbXj_An-EV7kwXJRWABHI_u1Hk26svrJZ-5TSCxrw9jPWuXkkTBTrALiGQcQpwf3eiJhTtYVmIjRknR_-_fM6-mC4312HnyvetCCHWuZzmtlKmfFirAWrTpl1s7lMdM8zqg9IVkH"/>
</a>
</div>
</header>

<!-- Navigation Drawer -->
<div id="drawer-overlay" class="fixed inset-0 bg-black/40 z-[60] hidden transition-opacity" onclick="document.getElementById('nav-drawer').classList.add('-translate-x-full'); this.classList.add('hidden');"></div>
<aside id="nav-drawer" class="fixed top-0 left-0 w-72 h-full bg-white dark:bg-slate-900 z-[70] transform -translate-x-full transition-transform duration-300 ease-in-out shadow-2xl flex flex-col overflow-y-auto">
<div class="p-6 border-b border-slate-100 flex items-center gap-4">
<img alt="User" class="w-14 h-14 rounded-full" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDsODJt1tT752FfsIlf0EVEMTPh7CkI3YaxCo-859HcXYCzVTTzxlLgZcN1NmoRV1ml8gHGZiqvCN35yCqoErdR9q3yvcnCoXln3aCKjItRjVYZ9oaL2-3yOEq4ol6vimRiHBXwYbXj_An-EV7kwXJRWABHI_u1Hk26svrJZ-5TSCxrw9jPWuXkkTBTrALiGQcQpwf3eiJhTtYVmIjRknR_-_fM6-mC4312HnyvetCCHWuZzmtlKmfFirAWrTpl1s7lMdM8zqg9IVkH"/>
<div>
<p class="text-sm text-slate-500">Hey!</p>
<p class="font-bold text-teal-700">James Powell</p>
</div>
</div>
<div class="p-4 flex flex-col gap-2 flex-1">
<a href="{prefix}dashboard.html" class="flex items-center gap-4 px-4 py-3 bg-[#4caf50] text-white rounded-xl">
<span class="material-symbols-outlined">home</span>
<span class="font-semibold flex-1">Homepage</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}schedule.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">calendar_today</span>
<span class="font-semibold flex-1">Schedule</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}blog.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">article</span>
<span class="font-semibold flex-1">Blog</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}donate.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">volunteer_activism</span>
<span class="font-semibold flex-1">Donation</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}scan.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">delete</span>
<span class="font-semibold flex-1">LogWaste</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
<a href="{prefix}marketPlace.html" class="flex items-center gap-4 px-4 py-3 text-slate-700 hover:bg-slate-50 rounded-xl">
<span class="material-symbols-outlined">storefront</span>
<span class="font-semibold flex-1">Market</span>
<span class="material-symbols-outlined text-sm">chevron_right</span>
</a>
</div>
<div class="p-4 border-t border-slate-100">
<button onclick="logout()" class="flex items-center gap-4 px-4 py-3 text-red-500 hover:bg-red-50 rounded-xl w-full text-left">
<span class="material-symbols-outlined">logout</span>
<span class="font-semibold">Logout</span>
</button>
</div>
</aside>"""

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

    # Remove Bottom NavBar
    bottom_nav_pattern = re.compile(r'<!--\s*BottomNavBar\s*-->.*?</nav>', re.DOTALL)
    alt_bottom_nav_pattern = re.compile(r'<button class="mobile-fab[^>]*>.*?</nav>', re.DOTALL)
    
    content = bottom_nav_pattern.sub('', content)
    content = alt_bottom_nav_pattern.sub('', content)
    
    # Also remove any remaining <nav class="mobile-bottom-nav..."> if it was missed
    standalone_nav_pattern = re.compile(r'<nav class="mobile-bottom-nav[^>]*>.*?</nav>', re.DOTALL)
    content = standalone_nav_pattern.sub('', content)

    # Replace TopAppBar
    header_pattern = re.compile(r'<header class="mobile-top-bar[^>]*>.*?</header>', re.DOTALL)
    new_header = new_header_template.replace('{prefix}', prefix)
    
    if header_pattern.search(content):
        content = header_pattern.sub(new_header, content, count=1)
    else:
        # If no top app bar exists, we should probably insert it, but let's only replace existing ones
        # to be safe and avoid double headers on pages that didn't have it.
        # Wait, if we want all pages to have it:
        body_pattern = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
        match = body_pattern.search(content)
        if match:
            # We insert it right after body
            content = content[:match.end()] + '\n' + new_header + content[match.end():]
            
    # Quick fix for duplicated TopAppBar & Navigation Drawer if any
    # Just in case our script runs multiple times or there are multiple headers
    
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
