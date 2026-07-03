import re

with open(r'C:\Users\PC\Documents\2026FIFA\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update R14: st from "live" to "done", update hl
old_r14 = '''{id:"R14",g:"KO",r:4,t:"7/4 02:00",h:"澳大利亚",a:"埃及",s:"1-1",st:"live",hl:"🔴 澳大利亚1-1埃及（58'）：Emam Ashour 13'头球破门助埃及先声夺人，澳大利亚下半场扳平比分，双方暂1-1僵持（ESPN确认2nd Half 58'）",pred:{locked:true,ph:1,pa:1,confidence:54,tag:"谨慎看平",reason:"澳大利亚身体和定位球优势明显，埃及依靠萨拉赫与边路速度有反击威胁，90分钟胜负很难拉开。",basis:["澳洲定位球","萨拉赫","低比分"]}}'''
new_r14 = '''{id:"R14",g:"KO",r:4,t:"7/4 02:00",h:"澳大利亚",a:"埃及",s:"1-1",st:"done",hl:"⚽ 澳大利亚1-1埃及（点球2-4）：Emam Ashour 13'首开纪录，Mohamed Hany 55'乌龙扳平，双方120分钟战平1-1；点球大战埃及4-2胜出，队史首次晋级世界杯淘汰赛16强。R23 已同步为「待定(R15胜者) vs 埃及」。",pred:{locked:true,ph:1,pa:1,confidence:54,tag:"谨慎看平",reason:"澳大利亚身体和定位球优势明显，埃及依靠萨拉赫与边路速度有反击威胁，90分钟胜负很难拉开。",basis:["澳洲定位球","萨拉赫","低比分"]}}'''
assert old_r14 in content, "R14 old string not found!"
content = content.replace(old_r14, new_r14, 1)
print("✓ R14 updated")

# 2. Update R23: a from "待定(R14胜者)" to "埃及"
old_r23 = '''{id:"R23",g:"KO",r:5,t:"7/8 00:00",h:"待定(R15胜者)",a:"待定(R14胜者)",st:"upcoming",hl:"🏟️ 梅赛德斯-奔驰球场·亚特兰大 · R15胜者 vs R14胜者"}'''
new_r23 = '''{id:"R23",g:"KO",r:5,t:"7/8 00:00",h:"待定(R15胜者)",a:"埃及",st:"upcoming",hl:"🏟️ 梅赛德斯-奔驰球场·亚特兰大 · R15胜者 vs 埃及"}'''
assert old_r23 in content, "R23 old string not found!"
content = content.replace(old_r23, new_r23, 1)
print("✓ R23 updated to Egypt")

# 3. Add log entry after the log-list opening div
log_entry = '''      <div class="log-list" id="updateLogList">
              <div class="log-item">
        <div class="log-time">2026-07-04 05:30</div>
        <div class="log-content"><span class="log-tag auto">赛果</span><strong>🏁 R14 完赛：埃及点球4-2淘汰澳大利亚，R23 已同步落位</strong> — 福福已根据 ESPN World Cup match center 与 BBC Sport Scores &amp; Fixtures 最新交叉复核：北京时间 7/4 02:00 开球的 32 强战 R14 已在开球超过 120 分钟后确认 <code>FT-Pens</code>，90 分钟与加时为 1-1，埃及点球大战 4-2 取胜晋级，完成队史世界杯淘汰赛首胜。本站已将 ALL_MATCHES 中 R14 从 <code>live</code> 切换为 <code>done</code>，保留常规时间比分 <code>1-1</code> 并重写赛果摘要，同时把 R23 从&quot;待定(R15胜者) vs 待定(R14胜者)&quot;更新为&quot;待定(R15胜者) vs 埃及&quot;。当前北京时间 05:30 不在 00:05-02:00 预测窗口内，本轮未新增预测，既有 locked 预测全部保留。</div>
      </div>
              <div class="log-item">
        <div class="log-time">2026-07-04 03:19</div>'''

old_log_start = '''      <div class="log-list" id="updateLogList">
              <div class="log-item">
        <div class="log-time">2026-07-04 03:19</div>'''

content = content.replace(old_log_start, log_entry, 1)
print("✓ Log entry added")

with open(r'C:\Users\PC\Documents\2026FIFA\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("✓ File written successfully")
