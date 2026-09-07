# -*- coding: utf-8 -*-
import os, re
ROOT = os.path.expanduser('~/mnt/Version 2')

CSS = '''.mmenu__phone{display:inline-flex;align-items:center;gap:9px;margin-top:28px;
  font-family:var(--font-display);font-size:20px;font-weight:700;color:var(--navy);
  transition:color .25s var(--ease),transform .3s var(--ease);}
.mmenu__phone:hover{color:var(--blue);}
.mmenu__phone svg{width:17px;height:17px;fill:currentColor;flex:0 0 auto;}
.mmenu__phone + .btn{margin-top:16px;}
'''
CSS_ANCHOR = '.mobile-menu .btn{margin-top:28px;justify-content:center;}\n'

PHONE = ('  <a class="mmenu__phone" href="tel:+61284597882">'
         '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
         '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.24 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .57 3.6 1 1 0 0 1-.25 1z"/>'
         '</svg>+61 2 8459 7882</a>\n')

BTN = re.compile(r'( *)(<a class="btn btn--primary" href="(?:\.\./)*book\.html"><span>Book a Free IT Review</span></a>\n</div>)')

n = 0; skipped = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d != 'dump']
    for f in sorted(fn):
        if not f.endswith('.html'): continue
        p = os.path.join(dp, f); s = open(p, encoding='utf-8').read()
        if 'mmenu__phone' in s: skipped.append((p,'already')); continue
        if CSS_ANCHOR not in s or not BTN.search(s): skipped.append((p,'anchor')); continue
        s = s.replace(CSS_ANCHOR, CSS_ANCHOR + CSS, 1)
        s = BTN.sub(lambda m: PHONE + m.group(1) + m.group(2), s, count=1)
        open(p, 'w', encoding='utf-8', newline='').write(s)
        n += 1
print('updated:', n, ' skipped:', len(skipped), skipped[:5])
