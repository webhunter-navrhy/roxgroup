#!/usr/bin/env python3
"""Sestaví web ROX GROUP: src/layout.html + src/pages/*.html → statické stránky, assety s ?v= hashem."""
import hashlib, json, pathlib, re, shutil

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / 'src'

# Kontaktní údaje — doplnit skutečné před spuštěním
PHONE = '+420 000 000 000'
EMAIL = 'info@roxgroup.cz'

shutil.copy(SRC / 'style.css', ROOT / 'assets/style.css')
shutil.copy(SRC / 'main.js', ROOT / 'assets/main.js')
for f in (ROOT / 'brand').glob('*.svg'):
    shutil.copy(f, ROOT / 'assets' / f.name)

h = lambda p: hashlib.md5((ROOT / p).read_bytes()).hexdigest()[:8]
common = {
    'v_css': h('assets/style.css'), 'v_js': h('assets/main.js'), 'v_fav': h('assets/favicon.svg'),
    'v_logo': h('assets/logo-horizontal-dark.svg'),
    'phone': PHONE, 'phone_raw': PHONE.replace(' ', ''), 'email': EMAIL,
}
layout = (SRC / 'layout.html').read_text()

for page in sorted((SRC / 'pages').glob('*.html')):
    raw = page.read_text()
    meta = json.loads(re.match(r'<!--(.*?)-->', raw, re.S).group(1))
    content = raw[raw.index('-->') + 3:]
    vals = dict(common, title=meta['title'], desc=meta['desc'], root=meta['root'], content=content)
    for key in ('home', 'sluzby', 'onas', 'kontakt'):
        vals['cur_' + key] = 'aria-current="page"' if meta['cur'] == key else ''
    html = layout
    for _ in range(2):  # content obsahuje vlastní {{…}}
        html = re.sub(r'\{\{(\w+)\}\}', lambda m: vals.get(m.group(1), m.group(0)), html)
    out = ROOT / meta['out']
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print('✓', meta['out'])
