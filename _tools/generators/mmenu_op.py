# -*- coding: utf-8 -*-
import os, re
ROOT = os.path.expanduser('~/mnt/public')
PAT = re.compile(r'([ \t]*)<a class="mmenu__link" href="((?:\.\./)*)one-partner\.html">Why One Partner</a>\n')

ITEMS = [
 ('one-partner.html',            'One Partner Overview'),
 ('one-partner.html#here-for',   'What We&rsquo;re Here For'),
 ('one-partner.html#coverage',   'See Coverage'),
 ('one-partner.html#advantages', 'See The Advantages'),
 ('one-partner.html#three-teams','What One Partner Covers'),
]

def build(ind, pre):
    L = [ind + '<div class="mmenu__group">',
         ind + '  <button class="mmenu__toggle" aria-expanded="false">Why One Partner <i class="chev"></i></button>',
         ind + '  <div class="mmenu__sub">']
    for href, label in ITEMS:
        L.append(ind + '    <a href="%s%s">%s</a>' % (pre, href, label))
    L += [ind + '  </div>', ind + '</div>']
    return '\n'.join(L) + '\n'

n = 0; skip = 0
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('dump',)]
    for f in sorted(fn):
        if not f.endswith('.html'): continue
        p = os.path.join(dp, f)
        s = open(p, encoding='utf-8').read()
        if 'Why One Partner <i class="chev"></i>' in s and 'mmenu__toggle' in s.split('<nav class="mmenu">')[-1][:2000]:
            pass
        m = PAT.search(s)
        if not m:
            skip += 1; continue
        s2 = PAT.sub(lambda mm: build(mm.group(1), mm.group(2)), s, count=1)
        open(p, 'w', encoding='utf-8', newline='').write(s2)
        n += 1
print('updated:', n, ' no-match:', skip)
