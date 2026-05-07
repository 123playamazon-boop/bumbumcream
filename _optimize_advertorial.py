"""
2 cosmetic fixes for advertorial:
1. Press logos: remove blue link-look, add cursor:default
2. First CTA: subtle pulse animation to draw eye
"""
import os
BASE = os.path.dirname(os.path.abspath(__file__))
fpath = os.path.join(BASE, 'index.html')
content = open(fpath).read()
changes = []

# ============ FIX 1: press logos non-clickable look ============
# Old: font-weight:600;color:#2e4a6b (blue, bold = looks like link)
# New: muted gray, normal weight, cursor:default
old_press_css = '.as-reported .ar-sources span{margin:0 10px;white-space:nowrap;display:inline-block;font-weight:600;color:#2e4a6b}'
new_press_css = '.as-reported .ar-sources span{margin:0 10px;white-space:nowrap;display:inline-block;font-weight:500;color:#666;cursor:default;pointer-events:none}'
if old_press_css in content:
    content = content.replace(old_press_css, new_press_css, 1)
    changes.append('Press logos: removed blue/bold (no longer look clickable), added cursor:default + pointer-events:none')

# ============ FIX 2: subtle pulse on first CTA to draw attention ============
# Find the existing .cta CSS or inject @keyframes + animation
# Look for the .cta class definition
pulse_css = '''
  /* Pulse animation on primary CTA to capture attention */
  @keyframes ctaPulse{
    0%,100%{box-shadow:0 4px 14px rgba(204,85,0,.35)}
    50%{box-shadow:0 4px 24px rgba(204,85,0,.6),0 0 0 6px rgba(204,85,0,.08)}
  }
  .cta-wrap .cta{animation:ctaPulse 2.4s ease-in-out infinite}
  .cta-wrap .cta:hover{animation-play-state:paused}
'''

# Insert this CSS right before </style> of the head
# Find the first </style> tag and insert before it
if 'ctaPulse' not in content:
    # Insert before first </style>
    idx = content.find('</style>')
    if idx > 0:
        content = content[:idx] + pulse_css + content[idx:]
        changes.append('First CTA: added subtle pulse animation (2.4s loop) for visibility')

open(fpath, 'w').write(content)
print(f'Updated index.html ({len(content)} bytes)')
for c in changes:
    print(f'  + {c}')

# Verify CSS is present
final = open(fpath).read()
print(f"\nVerification:")
print(f"  pointer-events:none on press: {'pointer-events:none' in final}")
print(f"  ctaPulse keyframe present: {'ctaPulse' in final}")
