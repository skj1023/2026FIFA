import re, json, urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

html = Path('index.html').read_text(encoding='utf-8')
m = re.search(r'const ALL_MATCHES\s*=\s*(\[[\s\S]*?\n\]);', html)
if not m:
    raise SystemExit('ALL_MATCHES not found')
arr = json.loads(re.sub(r'(\w+):', r'"\1":', m.group(1).replace("'", '"')))

now = datetime.now(ZoneInfo('Asia/Shanghai'))
print('NOW_SH', now.isoformat())
counts = {}
for x in arr:
    counts[x.get('st','?')] = counts.get(x.get('st','?'), 0) + 1
print('COUNTS', json.dumps(counts, ensure_ascii=False))
print('TOTAL', len(arr))
print('LAST_DONE', json.dumps([x['id'] for x in arr if x.get('st')=='done'][-8:], ensure_ascii=False))
print('UPCOMING', json.dumps([{'id':x['id'],'t':x.get('t'),'h':x.get('h'),'a':x.get('a'),'st':x.get('st')} for x in arr if x.get('st')!='done'][:12], ensure_ascii=False))

url='https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard'
with urllib.request.urlopen(url, timeout=30) as r:
    data=json.load(r)
print('ESPN_EVENTS', len(data.get('events', [])))
for ev in data.get('events', []):
    comp=ev['competitions'][0]
    status=comp['status']['type']
    teams=[c['team']['displayName'] for c in comp['competitors']]
    score='-'.join([c.get('score','') for c in comp['competitors']])
    print('EVENT', json.dumps({'id':ev['id'],'date':ev['date'],'name':ev['name'],'shortName':ev.get('shortName'),'status':status.get('description'),'detail':comp['status'].get('displayClock'),'state':status.get('state'),'completed':status.get('completed'),'teams':teams,'score':score}, ensure_ascii=False))
