#!/usr/bin/env python3
"""Update 2026 World Cup page: R08→live, predictions for R17/R18, log entry."""

import re
import json

with open(r'C:\Users\PC\Documents\2026FIFA\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update R08 (England vs Congo DR) - 0-1 at HT live
# Current: {id:"R08",g:"KO",r:4,t:"7/2 00:00",h:"英格兰",a:"刚果(金)",st:"upcoming",hl:"🏟️ 梅赛德斯-奔驰球场·亚特兰大 · L1 vs K3 · 英格兰7分L组头名出线；刚果(金)4分位列K组第三并跻身最佳第3名",pred:{...}}

old_r08 = '''{id:"R08",g:"KO",r:4,t:"7/2 00:00",h:"英格兰",a:"刚果(金)",st:"upcoming",hl:"🏟️ 梅赛德斯-奔驰球场·亚特兰大 · L1 vs K3 · 英格兰7分L组头名出线；刚果(金)4分位列K组第三并跻身最佳第3名",pred:{locked:true,ph:2,pa:0,confidence:76,tag:"英格兰稳胜",reason:"英格兰阵容厚度和定位球威胁明显更强，刚果(金)需要极高效率反击才有机会制造悬念。",basis:["阵容厚度","定位球","凯恩"]}}'''

new_r08 = '''{id:"R08",g:"KO",r:4,t:"7/2 00:00",h:"英格兰",a:"刚果(金)",s:"0-1",st:"live",hl:"🔴 半场英格兰0-1刚果(金)：Cipenga 7'闪击破门，刚果(金)稳守反击领先，贝林厄姆19'染黄",pred:{locked:true,ph:2,pa:0,confidence:76,tag:"英格兰稳胜",reason:"英格兰阵容厚度和定位球威胁明显更强，刚果(金)需要极高效率反击才有机会制造悬念。",basis:["阵容厚度","定位球","凯恩"]}}'''

assert old_r08 in html, "R08 old string not found!"
html = html.replace(old_r08, new_r08)

# 2. Add preds for R17 and R18 (no pred currently, need to add them before the closing bracket)
# R17: Canada vs Morocco (7/5 01:00 CST)
# R18: Paraguay vs France (7/5 05:00 CST)

r17_old = '''{id:"R17",g:"KO",r:5,t:"7/5 01:00",h:"加拿大",a:"摩洛哥",st:"upcoming",hl:"🏟️ NRG球场·休斯顿 · 加拿大 vs 摩洛哥 · R01/R04胜者已全部落位"}'''
r17_new = '''{id:"R17",g:"KO",r:5,t:"7/5 01:00",h:"加拿大",a:"摩洛哥",st:"upcoming",hl:"🏟️ NRG球场·休斯顿 · 加拿大 vs 摩洛哥 · R01/R04胜者已全部落位",pred:{date:"2026-07-01",ph:1,pa:1,winner:"d",confidence:58,tag:"谨慎看平",basis:["东道主气势","摩洛哥韧性","点球气焰"],reason:"加拿大淘汰赛首轮1-0绝杀南非士气正盛，东道主主场氛围不可小觑；摩洛哥点球淘汰荷兰韧劲十足，防守纪律性强。双方实力接近、风格各异，90分钟可能难分胜负。",sources:["FIFA","ESPN","Bing News"],locked:true}}'''

r18_old = '''{id:"R18",g:"KO",r:5,t:"7/5 05:00",h:"巴拉圭",a:"法国",st:"upcoming",hl:"🏟️ 林肯金融球场·费城 · 巴拉圭 vs 法国 · R03/R06 胜者已全部落位"}'''
r18_new = '''{id:"R18",g:"KO",r:5,t:"7/5 05:00",h:"巴拉圭",a:"法国",st:"upcoming",hl:"🏟️ 林肯金融球场·费城 · 巴拉圭 vs 法国 · R03/R06 胜者已全部落位",pred:{date:"2026-07-01",ph:0,pa:2,winner:"a",confidence:75,tag:"法国晋级",basis:["姆巴佩状态","法国攻击群","巴拉圭消耗大"],reason:"法国小组赛三战全胜攻防俱佳，姆巴佩和登贝莱边路冲击力对巴拉圭防线构成绝对威胁；巴拉圭刚经历点球大战消耗巨大，面对高卢军团的持续压迫恐难招架。",sources:["FIFA","ESPN","Bing News"],locked:true}}'''

assert r17_old in html, "R17 old string not found!"
html = html.replace(r17_old, r17_new)

assert r18_old in html, "R18 old string not found!"
html = html.replace(r18_old, r18_new)

# 3. Add log entry
# Find the last log-item and insert our new one after it
# Let's find a good insertion point. Last log should be from 7/1 14:13
log_new = '''      <div class=\"log-item\">
        <div class=\"log-time\">2026-07-02 00:50</div>
        <div class=\"log-content\"><span class=\"log-tag auto\">赛况</span><strong>🔴 R08 已切换 live：英格兰0-1刚果(金)（半场）</strong> — 福福根据 ESPN World Cup 官方数据复核：北京时间 7/2 00:00 开球的 32 强战 R08 英格兰vs刚果(金)当前半场结束，Cipenga 7' 闪击破门、贝林厄姆染黄；ESPN 确认半场比分 0-1。本站已将 R08 从 <code>upcoming</code> 切换为 <code>live</code>。同时，为 7/5 的两场 16 强战（R17 加拿大vs摩洛哥、R18 巴拉圭vs法国）生成了 AI 预测。当前北京时间 00:50 在 00:05-02:00 预测窗口内，已按站点规则为未来 3 天（7/3~7/5）中尚无 locked 预测的比赛生成预测。</div>
      </div>'''

# Find the position before the closing </div> of the log-list
# The log-list ends before the pattern for the next section. Let me find "get_decks"
# Actually, let me just find where the last log-item ends and insert after it
# Looking at the HTML, the log-list ends around line 790+
# Let me find a reliable anchor

# Find the last log-item div and insert before the closing tag of the main log-wrap div
# Simpler: find a pattern that uniquely identifies where log items end
log_insert_pattern = '          <div class=\"log-content\"><span class=\"log-tag auto\">赛果</span><strong>🏁 R07 完赛：墨西哥 2-0 厄瓜多尔，R20 主队已同步落位</strong> — 福福已根据 ESPN World Cup scoreboard 与 BBC Sport Scores &amp; Fixtures 交叉复核：北京时间 7/1 09:00 开球的 R07 现已 Full time，墨西哥 2-0 淘汰厄瓜多尔晋级。本站已将 ALL_MATCHES 中 R07 从 <code>live</code> 切换为 <code>done</code>，补写赛果摘要，并把 7/6 的 R20 从“待定(R07胜者) vs 待定(R08胜者)”同步更新为“墨西哥 vs 待定(R08胜者)”。当前北京时间 14:13 不在 00:05-02:00 预测窗口内，本轮未新增预测，既有 locked 预测全部保留。</div>\n      </div>'

# We need the log entry after this. Insert after the matching closing </div>
# Replace that full pattern with itself + new log entry
new_log_section = log_insert_pattern + '\n' + log_new

# But this might be too fragile. Let me try a different approach - find the exact position
# Actually let me find the position of the closing </div> of the last log item

# Try to find the exact pattern and insert after
if log_insert_pattern in html:
    idx = html.find(log_insert_pattern) + len(log_insert_pattern)
    # Check if there's a </div> closing the outer structure
    html = html.replace(log_insert_pattern, new_log_section)
    print("Log entry inserted successfully")
else:
    print("WARNING: Could not find anchor for log entry insertion!")
    # Try alternative - just find the last log-item
    import re
    matches = list(re.finditer(r'<div class="log-item">', html))
    if matches:
        # Find end of last log-item
        last_log_start = matches[-1].start()
        rest = html[last_log_start:]
        # Find closing </div> that closes this log-item
        depth = 0
        end_idx = 0
        for i, c in enumerate(rest):
            if rest[i:i+6] == '<div ' or rest[i:i+5] == '<div>':
                depth += 1
            elif rest[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end_idx = last_log_start + i + 6
                    break
        html = html[:end_idx] + '\n' + log_new + html[end_idx:]
        print("Log entry inserted via fallback method")

# 4. Write back
with open(r'C:\Users\PC\Documents\2026FIFA\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ index.html updated successfully")
print(f"  - R08: st=upcoming → live, s=0-1")
print(f"  - R17: pred added (Canada vs Morocco)")
print(f"  - R18: pred added (Paraguay vs France)")
print(f"  - Log entry added for 2026-07-02 00:50")
