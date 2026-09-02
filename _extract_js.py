import re
html = open('index.html', encoding='utf8').read()
m = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if m:
    js = m.group(1)
    open('_temp_check.js', 'w', encoding='utf8').write(js)
    print('JS extracted, length:', len(js))
else:
    print('NO SCRIPT FOUND')
