import re, sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all script content
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
js = '\n'.join(scripts)

# Write to temp file
with open('C:/Users/PC/Documents/2026FIFA/_tmp_syntax.js', 'w', encoding='utf-8') as f:
    f.write(js)

print(f'Extracted {len(js)} chars of JS from {len(scripts)} script blocks')
