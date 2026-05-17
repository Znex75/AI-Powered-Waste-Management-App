import os
import re

root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

header_content_template = """<header class="bg-background docked full-width top-0 sticky z-50">
<div class="flex items-center justify-between px-margin py-base w-full max-w-7xl mx-auto">
<div class="flex items-center gap-sm">
<button class="hover:bg-surface-container-low transition-colors p-base rounded-full active:scale-95 transition-transform duration-200">
<span class="material-symbols-outlined text-primary">menu</span>
</button>
<a href="{prefix}dashboard.html"><h1 class="font-headline-lg text-headline-lg text-primary tracking-tight">EcoCycle</h1></a>
</div>
<div class="flex items-center gap-md">
<nav class="hidden md:flex gap-md items-center">
<a class="text-on-surface-variant hover:text-primary font-label-md transition-colors" href="{prefix}recycle.html">Recycle</a>
<a class="text-on-surface-variant hover:text-primary font-label-md transition-colors" href="{prefix}events.html">Events</a>
<a class="text-on-surface-variant hover:text-primary font-label-md transition-colors" href="{prefix}tips.html">Tips</a>
<a class="text-on-surface-variant hover:text-primary font-label-md transition-colors" href="{prefix}community.html">Community</a>
</nav>
<a href="{prefix}Authentication/user.html">
<img alt="User Profile" class="w-10 h-10 rounded-full object-cover border-2 border-primary-container" data-alt="A professional headshot of a smiling eco-conscious person with a friendly expression. The lighting is soft and natural, emphasizing a bright and modern light-mode aesthetic. The background is a clean, minimalist urban environment with subtle green foliage, reflecting a sustainable lifestyle and organized brand personality." src="https://lh3.googleusercontent.com/aida-public/AB6AXuCtHU28OJFK66EQQxIOSWctmkicKo5_6xevayC8IVQ3tRzSagDpj5JkjtLWzGjwScs1I23E6KzmUxpvzQWD2Qm7_xTyYcw8yfDjMa-PK2IZ-7ssdEqfEoCEzpKQIWUDdJsr_aXJY4Vc7z5jJXvcak4KJjQX-Cucfoogu5u12OtD8EFl6E8e8voTlpOhyjYUkEfcdQzFVovKKYaMXnshhPr1gZCzqeQFPmvp5Oh6ywJShMU0um1TCHwHxPvMo7pPDMGLia6kdsHpvHN7"/>
</a>
</div>
</div>
</header>"""

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine prefix based on depth from root
    # e.g., Authentication/signUp.html -> depth 1 -> prefix "../"
    # Root files -> depth 0 -> prefix ""
    # android/app/src/main/assets/dashboard.html -> treat assets/ as root
    
    if 'android\\app\\src\\main\\assets' in filepath:
        rel_path = os.path.relpath(filepath, os.path.join(root_dir, 'android', 'app', 'src', 'main', 'assets'))
    else:
        rel_path = os.path.relpath(filepath, root_dir)
        
    depth = rel_path.count(os.sep)
    prefix = "../" * depth

    new_header = header_content_template.replace('{prefix}', prefix)

    # Regex to find existing header and replace it, or insert after body
    # This regex assumes <header ... > ... </header>
    header_pattern = re.compile(r'<header[^>]*>.*?</header>', re.DOTALL)
    
    if header_pattern.search(content):
        # Replace existing header
        new_content = header_pattern.sub(new_header, content, count=1)
    else:
        # Find <body> tag and insert right after it
        body_pattern = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
        match = body_pattern.search(content)
        if match:
            new_content = content[:match.end()] + '\n' + new_header + content[match.end():]
        else:
            print(f"Warning: No body tag found in {filepath}")
            return

    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk(root_dir):
    # Exclude build directories
    if 'build' in root or '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            process_html_file(filepath)
