const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const newEntry = `                              <div class="log-item">
                   <div class="log-time">2026-09-02 16:42</div>
                    <div class="log-content"><span class="log-tag fix">巡检</span><strong>✅ 赛后全站一致性复核：104/104 完赛 · Wikipedia/FIFA/BBC 交叉确认</strong> — 福福按北京时间完成赛后巡检（距决赛完赛已逾 10 周）。确认：ALL_MATCHES 104/104 已完赛、0 场进行中、0 场 upcoming；决赛 FIN 西班牙 1-0 阿根廷（AET, Ferran Torres 106'）与 Wikipedia 决赛专题、FIFA 官方奖项页、BBC Sport 一致；季军赛 法国 4-6 英格兰正确；射手榜姆巴佩 10 球金靴（FIFA+BBC 确认蝉联金靴、历史射手王 22 球）、梅西 8 球、贝林厄姆/哈兰德 7 球、凯恩/登贝莱 6 球完整；首页 hero 冠军西班牙、已完赛 104 场正确；下一场倒计时与今日推荐已正确隐藏；信息页"本届世界杯已结束"正确；淘汰赛 32 场全部落位完毕无 TBD；小组积分榜与最佳第3名 allGroupsComplete=true 运行时为"最终排序"口径；JS 语法校验通过。本轮无赛果/对阵/文案变更。<!-- marker:cron-post-tournament-check-20260902-1642 --></div>
                  </div>
`;

// Use a regex that handles both \n and \r\n
const marker = 'id="updateLogList">';
const idx = html.indexOf(marker);
if (idx === -1) {
  console.log('FAIL: could not find updateLogList');
  process.exit(1);
}
const insertPos = idx + marker.length;
// Find the next newline after the marker
let nlPos = html.indexOf('\n', insertPos);
if (nlPos === -1) nlPos = insertPos;
else nlPos += 1; // include the newline

html = html.slice(0, nlPos) + newEntry + html.slice(nlPos);
fs.writeFileSync('index.html', html, 'utf8');
console.log('Log entry added. Verify:');
console.log(html.includes('marker:cron-post-tournament-check-20260902-1642'));
