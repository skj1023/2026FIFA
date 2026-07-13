from pathlib import Path
import re
html = Path('index.html').read_text(encoding='utf-8')
m = re.search(r'<script>([\s\S]*?)</script>\s*</body>', html)
if not m:
    raise SystemExit('inline script not found')
Path('_inline_check.js').write_text(m.group(1).strip()+'\n', encoding='utf-8')
print('wrote', len(m.group(1)), 'chars to _inline_check.js')
