import os
import re

root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

dark_mode_css = """
    /* Global Dark Mode Styles */
    html.dark body, html.dark .bg-mesh, html.dark .bg-surface {
      background-color: #0f172a !important;
      background-image: none !important;
      color: #f1f5f9 !important;
    }
    html.dark .bg-white {
      background-color: #1e293b !important;
    }
    html.dark .border-slate-100, html.dark .border-slate-50 {
      border-color: #334155 !important;
    }
    html.dark .text-slate-700, html.dark .text-on-surface, html.dark .text-slate-800 {
      color: #f1f5f9 !important;
    }
    html.dark .text-slate-500, html.dark .text-on-surface-variant, html.dark .text-outline {
      color: #94a3b8 !important;
    }
    html.dark .bg-slate-50 {
      background-color: #334155 !important;
    }
    html.dark aside#nav-drawer, html.dark header {
      background-color: #0f172a !important;
      border-color: #334155 !important;
    }
    html.dark #modal-backdrop + div {
      background-color: #1e293b !important;
      color: #f1f5f9 !important;
    }
    html.dark input {
      background-color: #0f172a !important;
      color: #f1f5f9 !important;
      border-color: #334155 !important;
    }
"""

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # If the CSS is not already injected, inject it before the first </style>
    if "/* Global Dark Mode Styles */" not in content and "</style>" in content:
        content = re.sub(r'(</style>)', dark_mode_css + r'\n\1', content, count=1)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected dark CSS into {filepath}")

for root, dirs, files in os.walk(root_dir):
    if 'build' in root or '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            process_html_file(filepath)
