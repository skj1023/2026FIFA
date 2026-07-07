from pathlib import Path
import re, json

html = Path('index.html').read_text(encoding='utf-8')

# Find ALL_MATCHES array using careful extraction
idx_start = html.find('const ALL_MATCHES = [')
if idx_start == -1:
    idx_start = html.find('ALL_MATCHES = [')
assert idx_start >= 0, 'ALL_MATCHES not found'

# Get the content after = [
arr_start = html.find('[', idx_start)
depth = 1
i = arr_start + 1
while depth > 0 and i < len(html):
    if html[i] == '[':
        depth += 1
    elif html[i] == ']':
        depth -= 1
    i += 1
arr_text = html[arr_start:i]
print(f"ALL_MATCHES array length: {len(arr_text)}")

# Parse each match object
matches = []
obj_start = 0
while True:
    ob_start = arr_text.find('{', obj_start)
    if ob_start < 0 or ob_start > len(arr_text):
        break
    depth = 1
    j = ob_start + 1
    while depth > 0 and j < len(arr_text):
        if arr_text[j] == '{':
            depth += 1
        elif arr_text[j] == '}':
            depth -= 1
        j += 1
    obj_text = arr_text[ob_start:j]
    
    def extract(k):
        m = re.search(r'"' + k + r'"\s*:\s*"([^"]*)"', obj_text)
        return m.group(1) if m else None
    
    id_ = extract('id')
    g = extract('g')
    st = extract('st')
    if id_ and g:
        matches.append((id_, g, st))
    
    obj_start = j

from collections import defaultdict
groups = defaultdict(list)
for mid, g, st in matches:
    groups[g].append((mid, st))

print("\nGroups (A-L):")
all_group_complete = True
for g in sorted(groups.keys()):
    if g in 'ABCDEFGHIJKL':
        items = groups[g]
        done = sum(1 for _, s in items if s == 'done')
        print(f'  {g}: {len(items)} matches, {done} done')
        if len(items) != 6 or done != 6:
            all_group_complete = False
            for mid, s in items:
                print(f'    {mid}: {s}')

print(f'\nAll 12 groups complete? {all_group_complete}')
print(f'Total matches parsed: {len(matches)}')
