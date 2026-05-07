"""
Remove sales-y alerts from the advertorial.
Keep editorial feel.
"""
import os, re

fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
content = open(fpath).read()
original_size = len(content)

removed = []

# ============================================
# 1. Remove urgency-bar (HIGH DEMAND countdown at top)
# ============================================
# HTML: <div class="urgency-bar">...HIGH DEMAND...profile match...</div>
m = re.search(r'<div class="urgency-bar">.*?</div>', content, re.DOTALL)
if m:
    content = content.replace(m.group(0), '', 1)
    removed.append('urgency-bar (HIGH DEMAND countdown)')

# Remove its CSS rules (.urgency-bar, .urgency-icon, .urgency-time, related media query)
content = re.sub(r'\s*\.urgency-bar[^}]*\}', '', content)
content = re.sub(r'\s*\.urgency-bar \.urgency-icon[^}]*\}', '', content)
content = re.sub(r'\s*\.urgency-bar \.urgency-time[^}]*\}', '', content)
content = re.sub(r'\s*@media\(max-width:560px\)\{\.urgency-bar[^}]*\}\}', '', content)

# Remove its JS (urgencyTime countdown)
content = re.sub(r'\(function\(\)\{var el=document\.getElementById\("urgencyTime"\).*?\}\)\(\);', '', content, flags=re.DOTALL)

# ============================================
# 2. Remove .breaking banner (BBL INDUSTRY IN PANIC red strip)
# ============================================
m = re.search(r'<div class="breaking">.*?</div>', content, re.DOTALL)
if m:
    content = content.replace(m.group(0), '', 1)
    removed.append('breaking banner (BBL INDUSTRY PANIC)')

content = re.sub(r'\s*\.breaking[^}]*\}', '', content)
content = re.sub(r'\s*\.breaking \.dot[^}]*\}', '', content)

# ============================================
# 3. Remove .live counter ("2,847 readers viewing")
# ============================================
m = re.search(r'<div class="live">.*?</div>', content, re.DOTALL)
if m:
    content = content.replace(m.group(0), '', 1)
    removed.append('live counter (X readers viewing right now)')

content = re.sub(r'\s*\.live[^}]*\}', '', content)

# Remove liveCount script
content = re.sub(r'\(function\(\)\{var el=document\.getElementById\("liveCount"\).*?\}\)\(\);', '', content, flags=re.DOTALL)

# ============================================
# 4. Remove exit-overlay HTML block (entire popup)
# ============================================
m = re.search(r'<div class="exit-overlay" id="exitOverlay">.*?</div>\s*</div>', content, re.DOTALL)
if m:
    content = content.replace(m.group(0), '', 1)
    removed.append('exit popup HTML block')

# Remove exit-overlay CSS rules
exit_css_patterns = [
    r'\s*\.exit-overlay[^}]*\}',
    r'\s*\.exit-overlay\.show[^}]*\}',
    r'\s*\.exit-modal[^}]*\}',
    r'\s*\.exit-modal\s+h2[^}]*\}',
    r'\s*\.exit-modal\s+h2\s+span[^}]*\}',
    r'\s*\.exit-modal\s+p[^}]*\}',
    r'\s*\.exit-modal\s+\.exit-badge[^}]*\}',
    r'\s*\.exit-modal\s+\.exit-cta[^}]*\}',
    r'\s*\.exit-modal\s+\.exit-no[^}]*\}',
    r'\s*\.exit-close[^}]*\}',
    r'\s*\.exit-trust[^}]*\}',
]
for pat in exit_css_patterns:
    content = re.sub(pat, '', content)

# Remove exit popup JS (the IIFE with isMobile we already added — now obsolete)
content = re.sub(
    r'<script>\s*\(function\(\)\{\s*var isMobile = /iPhone\|iPad\|iPod\|Android.*?\}\)\(\);\s*</script>',
    '', content, flags=re.DOTALL
)

# Just in case original still there
content = re.sub(
    r'<script>\s*\(function\(\)\{\s*var shown = false; var modal = document\.getElementById\(\'exitOverlay\'\);.*?\}\)\(\);\s*</script>',
    '', content, flags=re.DOTALL
)

removed.append('exit popup CSS + JS')

# Save
open(fpath, 'w').write(content)

print(f'Original: {original_size} bytes')
print(f'After:    {len(content)} bytes')
print(f'Removed:  {original_size - len(content)} bytes')
print()
for r in removed:
    print(f'  - {r}')

# Verification
final = open(fpath).read()
print(f'\nVerification:')
print(f'  urgency-bar HTML:  {"<div class=\\"urgency-bar\\">" in final}')
print(f'  breaking HTML:     {"<div class=\\"breaking\\">" in final}')
print(f'  live counter HTML: {"<div class=\\"live\\">" in final}')
print(f'  exit-overlay HTML: {"<div class=\\"exit-overlay\\"" in final}')
print(f'  exitOverlay JS:    {"exitOverlay" in final}')
