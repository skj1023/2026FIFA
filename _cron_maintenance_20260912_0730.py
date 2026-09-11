from pathlib import Path

p = Path('index.html')
html = p.read_text(encoding='utf-8')
marker = 'marker:cron-full-check-20260912-0730'
if marker not in html:
    entry = '''                              <div class="log-item">
                              <div class="log-time">2026-09-12 07:30</div>
                              <div class="log-content"><span class="log-tag fix">巡检</span><strong>✅ 赛后全站一致性复核：104/104 完赛 · FIFA/ESPN/Al Jazeera/Sky Sports 轻量确认</strong> — 福福按北京时间完成赛后心跳巡检（距决赛完赛约 7 周 5 天，无实质数据变更）。外部轻量复核：FIFA 官方战报/Match Centre 继续确认决赛西班牙 1-0 阿根廷、Ferran Torres 106'、New York New Jersey Stadium、Match 104 与西班牙第二次夺冠；ESPN 战报继续显示 Spain 1-0 Argentina AET、Torres 106'、西班牙第二座世界杯冠军；Al Jazeera 奖项汇总继续确认姆巴佩 10 球金靴、Rodri 金球、Unai Simón 金手套；Sky Sports 同向确认 1-0 AET 与 Torres 106'。本地 ALL_MATCHES 104/104 完赛、0 live/upcoming、104 个唯一 id 无重复、分组 A-L 各 6 场 + KO 32 场、淘汰赛无 TBD、KO 预测无平局 winner；首页冠军西班牙、进度 104/104 (100%) 与“本届世界杯已结束”状态正确。本轮仅追加巡检日志，无赛果/对阵/预测/页面结构变更。<!-- marker:cron-full-check-20260912-0730 --></div>
                              </div>
'''
    target = '<div class="log-list" id="updateLogList">\n'
    if target not in html:
        raise SystemExit('log list anchor not found')
    html = html.replace(target, target + entry, 1)
    p.write_text(html, encoding='utf-8')
    print('UPDATED index.html with', marker)
else:
    print('NOOP marker already exists')
