#!/usr/bin/env python3
"""Extract JS from index.html for syntax check"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all script content
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
combined = '\n'.join(s for s in scripts if len(s.strip()) > 100)

with open('_cron_syntax_check.js', 'w', encoding='utf-8') as f:
    f.write(combined)

print(f'Extracted {len(combined)} chars of JS')
