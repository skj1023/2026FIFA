#!/usr/bin/env python3
"""Generate calendar.ics from FIFA World Cup HTML match data."""

import re
import json
import os
import sys
from datetime import datetime, timedelta
from calendar import timegm

# ===== Parse HTML to extract match data =====
def parse_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract ALL_MATCHES array as raw JS text
    m = re.search(r'const ALL_MATCHES\s*=\s*(\[[\s\S]*?\]);', content)
    if not m:
        raise ValueError("Cannot find ALL_MATCHES in HTML")
    
    raw = m.group(1)
    
    # Extract LOCATIONS object
    loc_m = re.search(r'const LOCATIONS\s*=\s*(\{[\s\S]*?\});', content)
    locations = {}
    if loc_m:
        locs = re.findall(r'"([^"]+)"\s*:\s*"([^"]*)"', loc_m.group(1))
        for k, v in locs:
            locations[k] = v
    
    # Parse each match object from JS array
    # Each match: {id:"A1",g:"A",r:1,t:"6/12 03:00",h:"Mexico",a:"South Africa",s:"2-0",st:"done",hl:"..."}
    matches = []
    # Split by { and parse each
    items = re.findall(r'\{([^}]+)\}', raw)
    
    for item in items:
        match = {}
        # Extract key:value pairs
        pairs = re.findall(r'(\w+)\s*:\s*(?:"([^"]*)"|([\d.]+)|true|false|null)', item)
        for key, str_val, num_val in pairs:
            val = str_val if str_val != '' else num_val
            match[key] = val
        
        if 'id' in match and 't' in match:
            # Only include upcoming and done matches that have time
            match['st'] = match.get('st', 'upcoming')
            matches.append(match)
    
    return matches, locations

def parse_match_time(time_str, base_year=2026):
    """Parse 'M/d HH:MM' to datetime (Beijing time, GMT+8)."""
    parts = time_str.strip().split(' ')
    if len(parts) < 2:
        return None
    date_part, time_part = parts[0], parts[1]
    m, d = date_part.split('/')
    h, mi = time_part.split(':')
    try:
        dt = datetime(int(base_year), int(m), int(d), int(h), int(mi))
        return dt
    except:
        return None

def ics_escape(s):
    if not s:
        return ''
    s = str(s)
    s = s.replace('\\', '\\\\')
    s = s.replace(';', '\\;')
    s = s.replace(',', '\\,')
    s = s.replace('\n', '\\n')
    return s

def ics_date(dt):
    """Format datetime for ICS: YYYYMMDDTHHMMSS."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%Y%m%dT%H%M%S')

def generate_ics(matches, locations):
    """Generate complete ICS content for all matches."""
    lines = []
    lines.append('BEGIN:VCALENDAR')
    lines.append('VERSION:2.0')
    lines.append('PRODID:-//福福//FIFA 2026 World Cup//ZH')
    lines.append('CALSCALE:GREGORIAN')
    lines.append('METHOD:PUBLISH')
    lines.append('X-WR-CALNAME:2026 FIFA World Cup 世界杯全部赛程')
    lines.append('X-WR-TIMEZONE:Asia/Shanghai')
    lines.append('X-PUBLISHED-TTL:PT1H')
    
    # Sort by time
    valid_matches = []
    for m in matches:
        dt = parse_match_time(m.get('t', ''))
        if dt:
            valid_matches.append((dt, m))
    
    valid_matches.sort(key=lambda x: x[0])
    
    uid_base = int(datetime.now().timestamp())
    uid_counter = 0
    
    for dt, m in valid_matches:
        end = dt + timedelta(hours=2, minutes=15)  # 2h15m for matches
        home = m.get('h', '?')
        away = m.get('a', '?')
        grp = m.get('g', '?')
        rnd = m.get('r', '1')
        
        title = f"{home} vs {away} · 2026世界杯 {grp}组"
        loc_key = f"{home}vs{away}"
        venue = locations.get(loc_key, '待定')
        
        desc = f"2026 FIFA World Cup · {grp}组 第{rnd}轮\n{home} vs {away}"
        
        if m.get('st') == 'done' and m.get('s'):
            desc += f"\n\n最终比分：{home} {m['s']} {away}"
        
        uid_counter += 1
        uid = f"fifa2026-{m['id']}-{uid_base}@fifa.skj1023.top"
        
        lines.append('BEGIN:VEVENT')
        lines.append(f'UID:{uid}')
        lines.append(f'DTSTART:{ics_date(dt)}')
        lines.append(f'DTEND:{ics_date(end)}')
        lines.append(f'SUMMARY:{ics_escape(title)}')
        lines.append(f'DESCRIPTION:{ics_escape(desc)}')
        lines.append(f'LOCATION:{ics_escape(venue)}')
        lines.append('BEGIN:VALARM')
        lines.append('TRIGGER:-PT15M')
        lines.append('ACTION:DISPLAY')
        lines.append('DESCRIPTION:比赛即将开始')
        lines.append('END:VALARM')
        lines.append('END:VEVENT')
    
    lines.append('END:VCALENDAR')
    return '\r\n'.join(lines) + '\r\n'

def main():
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(repo_dir, 'index.html')
    ics_path = os.path.join(repo_dir, 'calendar.ics')
    
    if not os.path.exists(html_path):
        # Try parent or find it
        for p in [os.path.join(repo_dir, '..', 'index.html'), os.path.join(repo_dir, 'fifa_repo', 'index.html')]:
            if os.path.exists(p):
                html_path = p
                break
    
    print(f"Reading matches from: {html_path}")
    matches, locations = parse_html(html_path)
    print(f"Found {len(matches)} matches, {len(locations)} venues")
    
    ics_content = generate_ics(matches, locations)
    
    with open(ics_path, 'w', encoding='utf-8') as f:
        f.write(ics_content)
    
    print(f"Written {len(ics_content)} bytes to {ics_path}")
    print(f"Done! {len(matches)} events in calendar.")

if __name__ == '__main__':
    main()
