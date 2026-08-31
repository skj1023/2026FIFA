import json, re, sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('const ALL_MATCHES = [')
if idx < 0:
    print("ERROR: ALL_MATCHES not found")
    sys.exit(1)

arr_start = content.index('[', idx)
depth = 0
end = arr_start
for i in range(arr_start, len(content)):
    if content[i] == '[':
        depth += 1
    elif content[i] == ']':
        depth -= 1
        if depth == 0:
            end = i + 1
            break

block = content[idx:end]
with open('_tmp_cron_am.js', 'w', encoding='utf-8') as f:
    f.write(block + '\n')
    f.write("""
const done = ALL_MATCHES.filter(m => m.st === "done");
const live = ALL_MATCHES.filter(m => m.st === "live");
const upcoming = ALL_MATCHES.filter(m => m.st !== "done" && m.st !== "live");
console.log("Total:", ALL_MATCHES.length);
console.log("Done:", done.length, "Live:", live.length, "Upcoming:", upcoming.length);
console.log("\\n--- Last 10 done ---");
done.slice(-10).forEach(m => console.log(m.id, m.h, m.s||"", m.a, "|", m.t, "|", m.g));
console.log("\\n--- All upcoming ---");
upcoming.forEach(m => console.log(m.id, m.h, "vs", m.a, "|", m.t, "|", m.g, "|", m.st));
console.log("\\n--- Live ---");
live.forEach(m => console.log(m.id, m.h, m.s||"", m.a, "|", m.t, "|", m.g));
console.log("\\n--- FIN ---");
let fin = ALL_MATCHES.find(m=>m.id==="FIN");
if(fin) console.log(JSON.stringify(fin));
console.log("\\n--- 3RD ---");
let third = ALL_MATCHES.find(m=>m.id==="3RD");
if(third) console.log(JSON.stringify(third));
""")
print(f"OK, extracted {end-idx} chars")
