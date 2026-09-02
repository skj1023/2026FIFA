import re, json, sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const ALL_MATCHES\s*=\s*\[([\s\S]*?)\];', html)
if not m:
    print('ERROR: ALL_MATCHES not found')
    sys.exit(1)

raw = m.group(0)

# Count statuses
done = raw.count('st:"done"')
live = raw.count('st:"live"')
upcoming = raw.count('st:"upcoming"')
total = done + live + upcoming
print(f'Total: {total}, Done: {done}, Live: {live}, Upcoming: {upcoming}')

# Count matches by stage
ko = raw.count('g:"KO"')
group = total - ko
print(f'Group matches: {group}, KO matches: {ko}')

# Check for any TBD in KO
tbd_count = raw.count('待定') + raw.count('TBD')
print(f'TBD references in ALL_MATCHES: {tbd_count}')

# Check final match
fin = re.search(r'id:"FIN".*?s:"(.*?)".*?st:"(.*?)"', raw)
if fin:
    print(f'Final: {fin.group(1)} ({fin.group(2)})')

# Check 3rd place
third = re.search(r'id:"3RD".*?s:"(.*?)".*?st:"(.*?)"', raw)
if third:
    print(f'3rd place: {third.group(1)} ({third.group(2)})')

# Check SF matches
sf1 = re.search(r'id:"SF1".*?s:"(.*?)".*?st:"(.*?)"', raw)
sf2 = re.search(r'id:"SF2".*?s:"(.*?)".*?st:"(.*?)"', raw)
if sf1: print(f'SF1: {sf1.group(1)} ({sf1.group(2)})')
if sf2: print(f'SF2: {sf2.group(1)} ({sf2.group(2)})')

# Check QF matches
for qf_id in ['QF1','QF2','QF3','QF4']:
    qf = re.search(rf'id:"{qf_id}".*?s:"(.*?)".*?st:"(.*?)"', raw)
    if qf: print(f'{qf_id}: {qf.group(1)} ({qf.group(2)})')

# Extract SCORERS
sc = re.search(r'const SCORERS\s*=\s*(\{.*?\})', html, re.DOTALL)
if sc:
    scorers_raw = sc.group(1)
    # Check key players
    for name in ['姆巴佩','梅西','贝林厄姆','哈兰德','凯恩','登贝莱','奥亚萨瓦尔','萨卡']:
        pm = re.search(rf'"{name}":"(.*?)"', scorers_raw)
        if pm:
            print(f'SCORERS {name}: {pm.group(1)}')
        else:
            print(f'SCORERS {name}: NOT FOUND')

# Check hero matchCount
mc = re.search(r'id="matchCount">(\d+)', html)
if mc:
    print(f'Hero matchCount: {mc.group(1)}')

# Check playedCount
pc = re.search(r'id="playedCount">(\d+)', html)
if pc:
    print(f'Info playedCount: {pc.group(1)}')

# Check for "赛事已全部结束"
if '赛事已全部结束' in html:
    print('Scorers section: 赛后口径 ✓')
else:
    print('Scorers section: MISSING 赛后口径')

# Check for "本届世界杯已结束"
if '本届世界杯已结束' in html:
    print('Info tab: 赛后口径 ✓')
else:
    print('Info tab: MISSING 赛后口径')

# Check info final countdown text
fc_main_search = re.search(r'fc-title">(.*?)</div>', html)
if fc_main_search:
    print(f'Info countdown title: {fc_main_search.group(1)}')

# Verify all 104 matches have unique IDs
ids = re.findall(r'id:"(\w+)"', raw)
print(f'Unique match IDs: {len(set(ids))}, Total entries: {len(ids)}')
if len(set(ids)) != len(ids):
    from collections import Counter
    dupes = [k for k,v in Counter(ids).items() if v > 1]
    print(f'DUPLICATE IDs: {dupes}')
