import re, sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Count match states in ALL_MATCHES
am_start = content.find('const ALL_MATCHES = [')
am_end = content.find('];', am_start) + 2
am_content = content[am_start:am_end]

matches = re.findall(r'st:"(done|live|upcoming)"', am_content)
done = matches.count('done')
live = matches.count('live')
upcoming = matches.count('upcoming')
print(f'ALL_MATCHES status: done={done}, live={live}, upcoming={upcoming}, total={done+live+upcoming}')

# Check for any 'upcoming' or 'live' matches
upc_matches = re.findall(r'\{id:"([^"]+)"[^}]*st:"(upcoming|live)"', am_content)
if upc_matches:
    print(f'Non-done matches: {upc_matches}')
else:
    print('All matches are done - tournament complete')

# Check hero text
if '冠军：西班牙' in content:
    print('Hero: Champion Spain ✓')
if '已完赛 <strong id="matchCount">104</strong>' in content:
    print('Hero match count: 104 ✓')

# Check info tab
if '本届世界杯已结束' in content:
    print('Info tab: Post-tournament message ✓')

# Check SCORERS
sc_start = content.find('const SCORERS=')
if sc_start > 0:
    sc_end = content.find('};', sc_start) + 2
    sc = content[sc_start:sc_end]
    if '姆巴佩' in sc and '法国 10' in sc:
        print('SCORERS: Mbappe 10 ✓')
    if '梅西' in sc and '阿根廷 8' in sc:
        print('SCORERS: Messi 8 ✓')
    if '哈兰德' in sc and '挪威 7' in sc:
        print('SCORERS: Haaland 7 ✓')
    if '贝林厄姆' in sc and '英格兰 7' in sc:
        print('SCORERS: Bellingham 7 ✓')

# Check final match
if 'FIN' in am_content and '1-0 AET' in am_content:
    print('Final: Spain 1-0 Argentina AET ✓')

# Check 3rd place
if '3RD' in am_content and '4-6' in am_content:
    print('3rd place: France 4-6 England ✓')

# Check log markers
markers = re.findall(r'marker:([a-z0-9-]+-\d{8,})', content)
if markers:
    print(f'Latest markers: {markers[:3]}')

# Extract scripts for syntax check
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
with open('_cron_syntax_check.js', 'w', encoding='utf-8') as f:
    for s in scripts:
        if s.strip():
            f.write(s)
            f.write('\n')
print(f'\nExtracted {len(scripts)} script blocks for syntax check')
