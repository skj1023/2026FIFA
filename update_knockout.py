#!/usr/bin/env python3
"""
Update the 2026 FIFA World Cup page with knockout stage match data.
Adds all 32 knockout matches to ALL_MATCHES array and updates the bracket tab.
"""
import re, os, shutil

HTML_PATH = r'C:/Users/PC/Documents/2026FIFA/index.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# ===== 1. Generate knockout ALL_MATCHES entries =====
# Time conversions (local to Beijing UTC+8):
# UTC-7→UTC+8 = +15h, UTC-6→UTC+8 = +14h, UTC-5→UTC+8 = +13h, UTC-4→UTC+8 = +12h

# Round of 32 entries (16 matches)
# r:4 = 32强, g:"KO"
r32 = [
    # R01: June 28 12:00 PT (UTC-7) = June 29 03:00 BJ
    '{id:"R01",g:"KO",r:4,t:"6/29 03:00",h:"南非",a:"加拿大",st:"upcoming",hl:"🏟️ SoFi球场·英格尔伍德 · A2 vs B2 · 南非小组末轮1-0胜韩国后抢下第二；加拿大虽1-2负瑞士仍以净胜球优势出线"}',
    # R02: June 29 12:00 CT (UTC-5) = June 30 01:00 BJ
    '{id:"R02",g:"KO",r:4,t:"6/30 01:00",h:"巴西",a:"日本",st:"upcoming",hl:"🏟️ NRG球场·休斯顿 · C1 vs F2 · 巴西7分锁C组头名；日本4-0大胜突尼斯后有望力拼出线"}',
    # R03: June 29 16:30 ET (UTC-4) = June 30 04:30 BJ
    '{id:"R03",g:"KO",r:4,t:"6/30 04:30",h:"德国",a:"巴拉圭",st:"upcoming",hl:"🏟️ 吉列球场·福克斯堡 · E1 vs D3/3rd"}',
    # R04: June 29 19:00 CT (UTC-6) = June 30 09:00 BJ
    '{id:"R04",g:"KO",r:4,t:"6/30 09:00",h:"荷兰",a:"摩洛哥",st:"upcoming",hl:"🏟️ BBVA球场·瓜达卢佩 · F1 vs C2 · 荷兰5-1大胜瑞典登顶F组；摩洛哥4-2收官战后7分列C组第二"}',
    # R05: June 30 12:00 CT (UTC-5) = July 1 01:00 BJ
    '{id:"R05",g:"KO",r:4,t:"7/1 01:00",h:"科特迪瓦",a:"挪威",st:"upcoming",hl:"🏟️ AT&T球场·阿灵顿 · I2 vs E2"}',
    # R06: June 30 17:00 ET (UTC-4) = July 1 05:00 BJ
    '{id:"R06",g:"KO",r:4,t:"7/1 05:00",h:"法国",a:"瑞典",st:"upcoming",hl:"🏟️ 大都会球场·东卢瑟福 · I1 vs F2 · 法国两连胜提前晋级，姆巴佩状态火热；瑞典5-1大胜突尼斯后前景可期"}',
    # R07: June 30 19:00 CT (UTC-6) = July 1 09:00 BJ
    '{id:"R07",g:"KO",r:4,t:"7/1 09:00",h:"墨西哥",a:"待定(C/E第3)",st:"upcoming",hl:"🏟️ 阿兹特克球场·墨西哥城 · A1 vs 3rd Group C/E · 东道主墨西哥三战全胜9分强势出线"}',
    # R08: July 1 12:00 ET (UTC-4) = July 2 00:00 BJ
    '{id:"R08",g:"KO",r:4,t:"7/2 00:00",h:"待定(L组冠军)",a:"待定(I/J/K第3)",st:"upcoming",hl:"🏟️ 梅赛德斯-奔驰球场·亚特兰大 · L1 vs 3rd I/J/K"}',
    # R09: July 1 13:00 PT (UTC-7) = July 2 04:00 BJ
    '{id:"R09",g:"KO",r:4,t:"7/2 04:00",h:"比利时",a:"待定(A/I/J第3)",st:"upcoming",hl:"🏟️ 流明球场·西雅图 · G1/J2 vs 3rd A/I/J · 比利时前两轮0-0伊朗后需末轮确定头名"}',
    # R10: July 1 17:00 PT (UTC-7) = July 2 08:00 BJ
    '{id:"R10",g:"KO",r:4,t:"7/2 08:00",h:"美国",a:"波黑",st:"upcoming",hl:"🏟️ 利维球场·圣克拉拉 · D1 vs B3 · 东道主美国两连胜提前出线，主场迎战波黑"}',
    # R11: July 2 12:00 PT (UTC-7) = July 3 03:00 BJ
    '{id:"R11",g:"KO",r:4,t:"7/3 03:00",h:"西班牙",a:"待定(J组第二)",st:"upcoming",hl:"🏟️ SoFi球场·英格尔伍德 · H1 vs J2 · 西班牙4-0沙特后欲锁定头名"}',
    # R12: July 2 19:00 ET (UTC-4) = July 3 07:00 BJ
    '{id:"R12",g:"KO",r:4,t:"7/3 07:00",h:"待定(K组第二)",a:"待定(L组第二)",st:"upcoming",hl:"🏟️ BMO球场·多伦多 · K2 vs L2"}',
    # R13: July 2 20:00 PT (UTC-7) = July 3 11:00 BJ
    '{id:"R13",g:"KO",r:4,t:"7/3 11:00",h:"瑞士",a:"待定(G/J第3)",st:"upcoming",hl:"🏟️ BC Place·温哥华 · B1 vs 3rd G/J · 瑞士7分B组头名出线"}',
    # R14: July 3 13:00 CT (UTC-5) = July 4 02:00 BJ
    '{id:"R14",g:"KO",r:4,t:"7/4 02:00",h:"澳大利亚",a:"埃及",st:"upcoming",hl:"🏟️ AT&T球场·阿灵顿 · D2 vs G2"}',
    # R15: July 3 18:00 ET (UTC-4) = July 4 06:00 BJ
    '{id:"R15",g:"KO",r:4,t:"7/4 06:00",h:"阿根廷",a:"佛得角",st:"upcoming",hl:"🏟️ 硬石球场·迈阿密花园 · J1 vs H2 · 卫冕冠军阿根廷两连胜提前晋级，梅西状态火热"}',
    # R16: July 3 20:30 CT (UTC-5) = July 4 09:30 BJ
    '{id:"R16",g:"KO",r:4,t:"7/4 09:30",h:"待定(K组冠军)",a:"待定(E/I/L第3)",st:"upcoming",hl:"🏟️ 箭头球场·堪萨斯城 · K1 vs 3rd E/I/L"}',
]

# Round of 16 (8 matches)
# r:5 = 16强
r16 = [
    '{id:"R17",g:"KO",r:5,t:"7/5 01:00",h:"待定(R01胜者)",a:"待定(R04胜者)",st:"upcoming",hl:"🏟️ NRG球场·休斯顿 · R01胜者 vs R04胜者"}',
    '{id:"R18",g:"KO",r:5,t:"7/5 05:00",h:"待定(R03胜者)",a:"待定(R06胜者)",st:"upcoming",hl:"🏟️ 林肯金融球场·费城 · R03胜者 vs R06胜者"}',
    '{id:"R19",g:"KO",r:5,t:"7/6 04:00",h:"待定(R02胜者)",a:"待定(R05胜者)",st:"upcoming",hl:"🏟️ 大都会球场·东卢瑟福 · R02胜者 vs R05胜者"}',
    '{id:"R20",g:"KO",r:5,t:"7/6 08:00",h:"待定(R07胜者)",a:"待定(R08胜者)",st:"upcoming",hl:"🏟️ 阿兹特克球场·墨西哥城 · R07胜者 vs R08胜者"}',
    '{id:"R21",g:"KO",r:5,t:"7/7 03:00",h:"待定(R12胜者)",a:"待定(R11胜者)",st:"upcoming",hl:"🏟️ AT&T球场·阿灵顿 · R12胜者 vs R11胜者"}',
    '{id:"R22",g:"KO",r:5,t:"7/7 08:00",h:"待定(R10胜者)",a:"待定(R09胜者)",st:"upcoming",hl:"🏟️ 流明球场·西雅图 · R10胜者 vs R09胜者"}',
    '{id:"R23",g:"KO",r:5,t:"7/8 00:00",h:"待定(R15胜者)",a:"待定(R14胜者)",st:"upcoming",hl:"🏟️ 梅赛德斯-奔驰球场·亚特兰大 · R15胜者 vs R14胜者"}',
    '{id:"R24",g:"KO",r:5,t:"7/8 04:00",h:"待定(R13胜者)",a:"待定(R16胜者)",st:"upcoming",hl:"🏟️ BC Place·温哥华 · R13胜者 vs R16胜者"}',
]

# Quarterfinals (4 matches)
# r:6 = 1/4决赛
qf = [
    '{id:"QF1",g:"KO",r:6,t:"7/10 04:00",h:"待定(R17胜者)",a:"待定(R18胜者)",st:"upcoming",hl:"🏟️ 吉列球场·福克斯堡 · 上半区1/4决赛"}',
    '{id:"QF2",g:"KO",r:6,t:"7/11 03:00",h:"待定(R21胜者)",a:"待定(R22胜者)",st:"upcoming",hl:"🏟️ SoFi球场·英格尔伍德 · 下半区1/4决赛"}',
    '{id:"QF3",g:"KO",r:6,t:"7/12 05:00",h:"待定(R19胜者)",a:"待定(R20胜者)",st:"upcoming",hl:"🏟️ 硬石球场·迈阿密花园 · 上半区1/4决赛"}',
    '{id:"QF4",g:"KO",r:6,t:"7/12 09:00",h:"待定(R23胜者)",a:"待定(R24胜者)",st:"upcoming",hl:"🏟️ 箭头球场·堪萨斯城 · 下半区1/4决赛"}',
]

# Semifinals (2 matches)
# r:7 = 半决赛
sf = [
    '{id:"SF1",g:"KO",r:7,t:"7/15 03:00",h:"待定(QF1胜者)",a:"待定(QF2胜者)",st:"upcoming",hl:"🏟️ AT&T球场·阿灵顿 · 上半区半决赛"}',
    '{id:"SF2",g:"KO",r:7,t:"7/16 03:00",h:"待定(QF3胜者)",a:"待定(QF4胜者)",st:"upcoming",hl:"🏟️ 梅赛德斯-奔驰球场·亚特兰大 · 下半区半决赛"}',
]

# Third place + Final
# r:8 = 季军赛, r:9 = 决赛
third_final = [
    '{id:"3RD",g:"KO",r:8,t:"7/19 05:00",h:"待定(SF1负者)",a:"待定(SF2负者)",st:"upcoming",hl:"🏟️ 硬石球场·迈阿密花园 · 季军争夺战"}',
    '{id:"FIN",g:"KO",r:9,t:"7/20 03:00",h:"待定(SF1胜者)",a:"待定(SF2胜者)",st:"upcoming",hl:"🏆 大都会球场·东卢瑟福·纽约 · 2026世界杯决赛！"}',
]

# Build the knockout data block
ko_entries = []
ko_entries.append('\n')
ko_entries.append('  // ===== 淘汰赛 32强 (6.29-7.4) =====\n')
ko_entries.extend(f'  {e},\n' for e in r32)
ko_entries.append('  // ===== 16强 (7.5-7.8) =====\n')
ko_entries.extend(f'  {e},\n' for e in r16)
ko_entries.append('  // ===== 1/4决赛 (7.10-7.12) =====\n')
ko_entries.extend(f'  {e},\n' for e in qf)
ko_entries.append('  // ===== 半决赛 (7.15-7.16) =====\n')
ko_entries.extend(f'  {e},\n' for e in sf)
ko_entries.append('  // ===== 季军赛 + 决赛 (7.19-7.20) =====\n')
ko_entries.extend(f'  {e},\n' for e in third_final)

# Insert knockout entries before the closing `];` of ALL_MATCHES
old_matches_end = '];\n\n// 2022 World Cup top 8 rankings'
# But that might not be unique. Let me look for the right anchor.
# Actually, the ALL_MATCHES array ends at line 1481 with `];` and then line 1483 starts with `// 2022 World Cup`
# The last entry in ALL_MATCHES is the L6 match ending with `locked:true}}`

# Find the position right after the last L6 match entry
# The last entry before `];` is L6
new_all_matches = html.replace(
    '{id:"L6",g:"L",r:3,t:"6/28 05:00",h:"克罗地亚",a:"加纳",st:"upcoming",hl:"⚔️ L组收官战 · 克罗地亚力争出线名额",pred:{date:"2026-06-25",ph:1,pa:1,winner:"d",confidence:59,tag:"谨慎看平",basis:["中场控制","加纳速度","末轮压力"],reason:"克罗地亚更擅长中场控制，加纳则有更直接的速度与冲击，末轮都背着结果压力，比赛很可能在试探和转换之间拉成平局。",sources:["FIFA","ESPN","Bing News"],locked:true}}\n];',
    '{id:"L6",g:"L",r:3,t:"6/28 05:00",h:"克罗地亚",a:"加纳",st:"upcoming",hl:"⚔️ L组收官战 · 克罗地亚力争出线名额",pred:{date:"2026-06-25",ph:1,pa:1,winner:"d",confidence:59,tag:"谨慎看平",basis:["中场控制","加纳速度","末轮压力"],reason:"克罗地亚更擅长中场控制，加纳则有更直接的速度与冲击，末轮都背着结果压力，比赛很可能在试探和转换之间拉成平局。",sources:["FIFA","ESPN","Bing News"],locked:true}}\n' + ''.join(ko_entries) + '];'
)

# ===== 2. Update the bracket tab =====
bracket_new = '''<div class="tab-content" id="tab-bracket">
<div class="container tab-main">
  <section class="section">
    <div class="section-header">
      <h2 class="section-title">🏅 淘汰赛</h2>
      <span class="section-sub">32强 → 16强 → 8强 → 4强 → 🏆 冠军</span>
    </div>
    <div class="bracket-wrap">
      <h3>🏆 2026 世界杯 · 淘汰赛对阵表</h3>
      <p>北京时间 · 共32场淘汰赛 · 一场定胜负</p>
      <div class="bracket-stages">
        <div class="bracket-stage active">
          <div class="sn">🏁 小组赛</div>
          <div class="sv">48→32</div>
          <div class="sd">6.11-6.28</div>
        </div>
        <div class="bracket-stage">
          <div class="sn">32强</div>
          <div class="sv">32→16</div>
          <div class="sd">6.29-7.4</div>
        </div>
        <div class="bracket-stage">
          <div class="sn">16强</div>
          <div class="sv">16→8</div>
          <div class="sd">7.5-7.8</div>
        </div>
        <div class="bracket-stage">
          <div class="sn">1/4决赛</div>
          <div class="sv">8→4</div>
          <div class="sd">7.10-7.12</div>
        </div>
        <div class="bracket-stage">
          <div class="sn">半决赛</div>
          <div class="sv">4→2</div>
          <div class="sd">7.15-7.16</div>
        </div>
        <div class="bracket-stage">
          <div class="sn">🥉 季军赛</div>
          <div class="sv">🥉</div>
          <div class="sd">7.19</div>
        </div>
        <div class="bracket-stage">
          <div class="sn">🏆 决赛</div>
          <div class="sv">🏆</div>
          <div class="sd">7.20 纽约</div>
        </div>
      </div>
      <div id="knockoutMatchList"></div>
    </div>
  </section>
</div>
</div>'''

# Replace bracket tab content
# Find the old bracket tab div
old_bracket_pattern = r'<div class="tab-content" id="tab-bracket">.*?</div>\s*</div>\s*</div>'
# Use re.DOTALL for multi-line matching
new_html = re.sub(
    r'<div class="tab-content" id="tab-bracket">.*?</div>\s*</div>\s*</div>\s*</div>',
    bracket_new,
    new_all_matches,
    flags=re.DOTALL
)

# Verify the replacement worked
if 'tab-bracket' not in new_html:
    print("ERROR: bracket tab replacement failed!")
    sys.exit(1)

# ===== 3. Add the knockout match list rendering JS =====
# Find the initLogFilter function and add knockout rendering after it
# Actually, I'll add the knockout rendering function to the JS section

# Find the calendar ICS generation area or a good insertion point
# Let's add knockout match list rendering code near the end of the JS, before the </script> tag

knockout_js = '''
// ===== KNOCKOUT ROUND MATCH RENDERING =====
function renderKnockoutMatches() {
  let container = document.getElementById('knockoutMatchList');
  if (!container) return;
  let ko = ALL_MATCHES.filter(m => m.g === 'KO');
  let rounds = {
    4: {name:'32强', dates:'6.29-7.4', icon:'💥'},
    5: {name:'16强', dates:'7.5-7.8', icon:'⚔️'},
    6: {name:'1/4决赛', dates:'7.10-7.12', icon:'🔥'},
    7: {name:'半决赛', dates:'7.15-7.16', icon:'💫'},
    8: {name:'季军赛', dates:'7.19', icon:'🥉'},
    9: {name:'🏆 决赛', dates:'7.20', icon:'🏆'}
  };
  let html = '';
  let roundKeys = [4,5,6,7,8,9];
  for (let rk of roundKeys) {
    let info = rounds[rk];
    let matches = ko.filter(m => m.r === rk);
    if (!matches.length) continue;
    html += '<div class="section-header" style="margin-top:12px"><h3 class="section-title" style="font-size:.95rem">'+info.icon+' '+info.name+' · '+info.dates+'</h3></div>';
    html += '<div style="display:flex;flex-direction:column;gap:5px;margin-bottom:10px">';
    // Sort matches by time
    matches.sort((a,b) => {
      let ta = parseMatchTime(a.t), tb = parseMatchTime(b.t);
      return ta - tb;
    });
    for (let m of matches) {
      let hd = td(m.h), ad = td(m.a);
      let isDone = m.st === 'done';
      let scoreStr = isDone ? ('<span class="ms">'+m.s+'</span>') : '<span class="ms" style="color:var(--text-dim)">vs</span>';
      let statusClass = isDone ? 'done' : 'upcoming';
      let timeLabel = m.t + (isDone ? '' : '');
      html += '<div class="match-card '+statusClass+' fade-in" style="padding:8px 12px;font-size:.75rem">';
      html += '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">';
      html += '<span style="color:var(--text-dim);font-size:.68rem;min-width:72px">'+timeLabel+'</span>';
      html += '<span style="flex:1;display:flex;align-items:center;justify-content:center;gap:4px">';
      html += '<span class="tn">'+hd.fl+hd.nm+'</span>';
      html += scoreStr;
      html += '<span class="tn">'+ad.fl+ad.nm+'</span>';
      html += '</span>';
      html += '<a class="cal-icon" onclick="addToCalendar(\\''+m.id+'\\');event.stopPropagation();" title="添加到日历" style="flex-shrink:0">📅</a>';
      html += '</div>';
      if (m.hl && !isDone) {
        html += '<div style="color:var(--text-dim);font-size:.65rem;margin-top:3px;padding-left:80px">'+m.hl+'</div>';
      }
      html += '</div>';
    }
    html += '</div>';
  }
  container.innerHTML = html;
  // Fade in
  requestAnimationFrame(() => {
    container.querySelectorAll('.fade-in').forEach(el => el.classList.add('vis'));
  });
}
'''

# Insert knockout JS right before the closing </script>
new_html = new_html.replace('</script>', knockout_js + '\n</script>')

# ===== 4. Call renderKnockoutMatches in the main render function =====
# Add it after renderThirdPlace() and before initLogFilter()
# Actually find the main render function and add the call
# Look for 'renderThirdPlace' or 'initLogFilter' or the fade-in block

# Find the main render() function and add knockout rendering
# Look for patterns like: renderThirdPlace(); or renderProgress();
# Let's add it at the end of the render function, before the fade-in

old_render_end = '  // Fade-in\n  document.querySelectorAll(\'.fade-in\').forEach((el,i)=>{\n    setTimeout(()=>el.classList.add(\'vis\'),i*60);\n  });\n}'
new_render_end = '  // Knockout bracket\n  renderKnockoutMatches();\n  \n  // Fade-in\n  document.querySelectorAll(\'.fade-in\').forEach((el,i)=>{\n    setTimeout(()=>el.classList.add(\'vis\'),i*60);\n  });\n}'

if old_render_end in new_html:
    new_html = new_html.replace(old_render_end, new_render_end)
else:
    print("WARNING: Could not find render fade-in block to add knockout call")

# ===== 5. Add match card CSS for KO matches =====
# Already using existing .match-card classes, should work fine

# ===== 6. Update total match count in hero (104 total now) =====
new_html = new_html.replace(
    '<strong id="matchCount">48</strong> 场',
    '<strong id="matchCount">48</strong> 场'
)  # The matchCount will be auto-calculated by JS

# Verify the output
if 'R01' not in new_html:
    print("ERROR: R01 not found in output!")
elif 'FIN' not in new_html:
    print("ERROR: FIN not found in output!")
elif 'renderKnockoutMatches' not in new_html:
    print("ERROR: renderKnockoutMatches function not found!")
elif 'tab-bracket' not in new_html:
    print("ERROR: tab-bracket not found!")
else:
    print("All checks passed!")

# Write back
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Updated {HTML_PATH}")
print(f"Total knockout matches added: {len(r32) + len(r16) + len(qf) + len(sf) + len(third_final)}")