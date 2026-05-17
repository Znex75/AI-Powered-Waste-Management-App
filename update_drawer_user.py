import os
import re

root_dir = r"c:\Users\sundi\OneDrive\Desktop\Waste Management"

drawer_profile_template = """<div class="p-6 border-b border-slate-100 flex items-center gap-4">
<label for="drawer-avatar-upload" class="cursor-pointer relative group block flex-shrink-0">
  <img id="nav-drawer-avatar" alt="User" class="w-14 h-14 rounded-full object-cover group-hover:opacity-75 transition-opacity" src="https://placehold.net/avatar.png"/>
  <div class="absolute inset-0 flex items-center justify-center bg-black/40 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
    <span class="material-symbols-outlined text-white text-sm">edit</span>
  </div>
</label>
<input type="file" id="drawer-avatar-upload" accept="image/*" class="hidden" onchange="uploadDrawerAvatar(event)" />
<div>
<p class="text-sm text-slate-500">Hey!</p>
<p id="nav-drawer-name" class="font-bold text-teal-700">Loading...</p>
</div>
</div>"""

drawer_script_template = """
<script>
  document.addEventListener('DOMContentLoaded', async () => {
    try {
      if (!window.supabase) return;
      const supa = window.supabase.createClient(
        "https://eupolobairqsuzjnihkc.supabase.co",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1cG9sb2JhaXJxc3V6am5paGtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc0ODA5ODQsImV4cCI6MjA5MzA1Njk4NH0._rUClX25cP5g6N1SOnggotJe0mqL63jisqLjjz7ZWK4"
      );
      const { data: { session } } = await supa.auth.getSession();
      if (session && session.user) {
        const user = session.user;
        const nameEl = document.getElementById('nav-drawer-name');
        const avatarEl = document.getElementById('nav-drawer-avatar');
        
        if (nameEl) {
          nameEl.innerText = user.user_metadata?.name || user.email.split('@')[0];
        }
        if (avatarEl && user.user_metadata?.avatar_url) {
          avatarEl.src = user.user_metadata.avatar_url;
        }
      }
    } catch(err) {
      console.error("Error fetching user for drawer:", err);
    }

    // Apply dark mode theme if saved
    const isDark = localStorage.getItem('theme') === 'dark';
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  });

  async function uploadDrawerAvatar(event) {
    const file = event.target.files[0];
    if (!file || !window.supabase) return;

    try {
      const supa = window.supabase.createClient(
        "https://eupolobairqsuzjnihkc.supabase.co",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1cG9sb2JhaXJxc3V6am5paGtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc0ODA5ODQsImV4cCI6MjA5MzA1Njk4NH0._rUClX25cP5g6N1SOnggotJe0mqL63jisqLjjz7ZWK4"
      );

      const avatarEl = document.getElementById('nav-drawer-avatar');
      avatarEl.style.opacity = '0.5';

      const reader = new FileReader();
      reader.onload = async () => {
        const base64 = reader.result;
        
        const { error } = await supa.auth.updateUser({
          data: { avatar_url: base64 }
        });

        if (error) throw error;
        
        avatarEl.src = base64;
        avatarEl.style.opacity = '1';
      };
      reader.readAsDataURL(file);
    } catch (e) {
      console.error(e);
      alert("Failed to update avatar.");
      document.getElementById('nav-drawer-avatar').style.opacity = '1';
    }
  }
</script>
"""

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Replace the profile block using the known img structure since the wrapper could be different now
    # Actually, the user's prompt gave the exact img tag:
    # <img id="nav-drawer-avatar" alt="User" class="w-14 h-14 rounded-full object-cover" src="https://via.placeholder.com/150"/>
    # Let's replace the whole profile block
    profile_pattern = re.compile(r'<div class="p-6 border-b border-slate-100 flex items-center gap-4">\s*<img id="nav-drawer-avatar" alt="User" class="w-14 h-14 rounded-full object-cover" src="https://via\.placeholder\.com/150"/>\s*<div>\s*<p class="text-sm text-slate-500">Hey!</p>\s*<p id="nav-drawer-name" class="font-bold text-teal-700">Loading...</p>\s*</div>\s*</div>', re.DOTALL)
    
    if profile_pattern.search(content):
        content = profile_pattern.sub(drawer_profile_template, content, count=1)
    
    # Try to find and replace the old script block
    # The old script block starts with <script> and ends with </script> and contains "Error fetching user for drawer"
    # Note that it might now contain uploadDrawerAvatar as well
    old_script_pattern = re.compile(r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', async \(\) => \{.*?console\.error\("Error fetching user for drawer:", err\);.*?\}?\s*\}\);\s*(async function uploadDrawerAvatar.*?\}|)\s*</script>', re.DOTALL)
    
    if old_script_pattern.search(content):
        content = old_script_pattern.sub(drawer_script_template, content, count=1)
    else:
        # If not found, just inject it after aside
        aside_close_pattern = re.compile(r'(</aside>)')
        if "uploadDrawerAvatar" not in content and aside_close_pattern.search(content):
            content = aside_close_pattern.sub(r'\1' + drawer_script_template, content, count=1)
            
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated drawer user in {filepath}")

for root, dirs, files in os.walk(root_dir):
    if 'build' in root or '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            process_html_file(filepath)
