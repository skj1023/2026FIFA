import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const ALL_MATCHES\s*=\s*\[([\s\S]*?)\];', html)
raw = m.group(1)

# Find lines with 待定 or TBD in ALL_MATCHES only
lines = raw.split('\n')
for i, line in enumerate(lines):
    if '待定' in line or 'TBD' in line:
        # Find the match ID
        id_m = re.search(r'id:"(\w+)"', line)
        mid = id_m.group(1) if id_m else 'unknown'
        # Show a snippet
        idx = line.find('待定') if '待定' in line else line.find('TBD')
        start = max(0, idx - 30)
        end = min(len(line), idx + 40)
        print(f'Line {i}: match {mid}: ...{line[start:end]}...')
