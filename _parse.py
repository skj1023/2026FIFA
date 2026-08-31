import re, json, sys
with open('index.html','r',encoding='utf-8') as f:
    text = f.read()
m = re.search(r'const ALL_MATCHES\s*=\s*(\[.*?\]);', text, re.DOTALL)
if not m:
    print("NOT FOUND"); sys.exit(1)
js = m.group(1)
# fix JS object literal to JSON
js = re.sub(r'(\w+)\s*:', r'"\1":', js)
js = js.replace("'", '"')
try:
    arr = json.loads(js)
except:
    # try with more fixes
    js = js.replace('undefined', 'null')
    arr = json.loads(js)
done = [x for x in arr if x.get('st')=='done']
live = [x for x in arr if x.get('st')=='live']
upcoming = [x for x in arr if x.get('st')=='upcoming']
print(f"Total: {len(arr)}, Done: {len(done)}, Live: {len(live)}, Upcoming: {len(upcoming)}")
# Show next upcoming sorted by time
import datetime
def parse_t(t):
    try:
        return datetime.datetime.strptime('2026/'+t, '%Y/%m/%d %H:%M')
    except:
        return datetime.datetime(2099,1,1)
now = datetime.datetime(2026,9,1,2,20)  # approx current time CST
print("\n--- LIVE matches ---")
for x in live:
    print(json.dumps(x, ensure_ascii=False))
print("\n--- Upcoming (next 15) ---")
u = sorted(upcoming, key=lambda x: parse_t(x.get('t','')))
for x in u[:15]:
    print(json.dumps(x, ensure_ascii=False))
print("\n--- Last 10 done ---")
d = sorted(done, key=lambda x: parse_t(x.get('t','')), reverse=True)
for x in d[:10]:
    print(json.dumps(x, ensure_ascii=False))
