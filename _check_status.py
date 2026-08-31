#!/usr/bin/env python3
"""Check ALL_MATCHES status and current time."""
import re
from datetime import datetime, timezone, timedelta

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find ALL_MATCHES block
start = content.find('const ALL_MATCHES = [')
end = content.find('];', start) + 2
js_block = content[start:end]

# Count statuses
done_count = js_block.count('st:"done"')
upcoming_count = js_block.count('st:"upcoming"')
live_count = js_block.count('st:"live"')

print('ALL_MATCHES status counts:')
print(f'  done: {done_count}')
print(f'  upcoming: {upcoming_count}')
print(f'  live: {live_count}')
print(f'  total: {done_count + upcoming_count + live_count}')

# Current Beijing time
beijing_tz = timezone(timedelta(hours=8))
now_beijing = datetime.now(beijing_tz)
print(f'\nCurrent Beijing time: {now_beijing.strftime("%Y-%m-%d %H:%M:%S")}')

# Check FIN match
fin_match = re.search(r'\{id:"FIN"[^}]+\}', js_block)
if fin_match:
    print(f'\nFinal match data:')
    print(fin_match.group(0))

# Extract all match IDs and times for upcoming
upcoming_matches = re.findall(r'\{id:"([^"]+)"[^}]*t:"([^"]+)"[^}]*st:"upcoming"', js_block)
if upcoming_matches:
    print(f'\nUpcoming matches:')
    for mid, mtime in upcoming_matches:
        print(f'  {mid}: {mtime}')
else:
    print('\nNo upcoming matches found.')

# Check last 5 done matches
done_matches = re.findall(r'\{id:"([^"]+)"[^}]*st:"done"[^}]*t:"([^"]+)"', js_block)
if done_matches:
    print(f'\nLast 5 done matches:')
    for mid, mtime in done_matches[-5:]:
        print(f'  {mid}: {mtime}')
