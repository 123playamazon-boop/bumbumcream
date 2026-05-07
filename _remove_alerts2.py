"""More robust removal — find each block by line scanning."""
import os, re

fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
content = open(fpath).read()
lines = content.split('\n')
new_lines = []
removed_count = 0

i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Skip urgency-bar block
    if '<div class="urgency-bar">' in line:
        # Find closing </div>
        depth = line.count('<div') - line.count('</div>')
        i += 1
        while i < len(lines) and depth > 0:
            depth += lines[i].count('<div') - lines[i].count('</div>')
            i += 1
        removed_count += 1
        continue

    # Skip .breaking block (single line)
    if line.strip().startswith('<div class="breaking">'):
        i += 1
        removed_count += 1
        continue

    # Skip .live block
    if line.strip().startswith('<div class="live">'):
        i += 1
        removed_count += 1
        continue

    # Skip exit-overlay block (multi-line)
    if '<div class="exit-overlay" id="exitOverlay">' in line:
        depth = line.count('<div') - line.count('</div>')
        i += 1
        while i < len(lines) and depth > 0:
            depth += lines[i].count('<div') - lines[i].count('</div>')
            i += 1
        removed_count += 1
        continue

    new_lines.append(line)
    i += 1

content = '\n'.join(new_lines)

# Now also remove the exit popup JS IIFE
# The script tag pattern: <script>(function(){var isMobile=... or var shown=false; ... })();</script>
# Find <script> tags whose body references exitOverlay
def remove_script_tags_with(content, marker):
    out = []
    i = 0
    n = len(content)
    while i < n:
        idx = content.find('<script>', i)
        if idx < 0:
            out.append(content[i:])
            break
        end = content.find('</script>', idx)
        if end < 0:
            out.append(content[i:])
            break
        block = content[idx:end+9]
        if marker in block:
            out.append(content[i:idx])
            i = end + 9
        else:
            out.append(content[i:end+9])
            i = end + 9
    return ''.join(out)

content = remove_script_tags_with(content, 'exitOverlay')
content = remove_script_tags_with(content, 'urgencyTime')
content = remove_script_tags_with(content, 'liveCount')

open(fpath, 'w').write(content)

# Final verification
final = open(fpath).read()
print(f'Removed {removed_count} HTML blocks')
print(f'Final size: {len(final)} bytes')
print()
print('Verification (all should be 0 / False):')
print(f'  urgency-bar HTML:   {final.count(chr(60) + chr(100) + chr(105) + chr(118) + " class=" + chr(34) + "urgency-bar" + chr(34))}')
print(f'  breaking HTML:      {final.count(chr(60) + chr(100) + chr(105) + chr(118) + " class=" + chr(34) + "breaking" + chr(34))}')
print(f'  live HTML:          {final.count(chr(60) + chr(100) + chr(105) + chr(118) + " class=" + chr(34) + "live" + chr(34))}')
print(f'  exit-overlay HTML:  {final.count("exit-overlay" + chr(34))}')
print(f'  exitOverlay refs:   {final.count("exitOverlay")}')
print(f'  urgencyTime refs:   {final.count("urgencyTime")}')
print(f'  liveCount refs:     {final.count("liveCount")}')
