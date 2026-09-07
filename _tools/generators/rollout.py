# -*- coding: utf-8 -*-
"""Put the five mega panels into every page's header."""
import os, re, glob, sys

SITE  = os.path.expanduser('~/mnt/Version 2')
BUILD = os.path.expanduser('~/ocblog')
def rd(p): return open(p, encoding='utf-8').read()

CSS = rd(os.path.join(BUILD, 'g_mega_css.txt'))
NAV = rd(os.path.join(BUILD, 'g_mega_nav.txt'))
JS  = rd(os.path.join(BUILD, 'g_mega_js.txt'))

REL = re.compile(r'(href|src)="(?!https?:|//|/|#|mailto:|tel:|data:|\.\./)([^"]+)"')

os.chdir(SITE)
files = sorted(glob.glob('*.html') + glob.glob('service/*/index.html') +
               glob.glob('blog/*.html') + glob.glob('book/*.html') + glob.glob('contact/*.html'))

done, skipped, problems = [], [], []
for f in files:
    s = rd(f)
    if 'nav__item--mega' in s:
        skipped.append(f); continue
    if '<nav class="nav" aria-label="Main navigation">' not in s:
        problems.append((f, 'no main nav')); continue

    depth = f.count('/')
    pre = '../' * depth
    nav = REL.sub(lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2)), NAV) if depth else NAV

    # 1. nav contents
    a = s.index('<nav class="nav" aria-label="Main navigation">'); a = s.index('>', a) + 1
    b = s.index('    </nav>', a)
    s = s[:a] + nav + s[b:]

    # 2. css, before the first </style>
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]

    # 3. js, before </body>
    i = s.rindex('</body>'); s = s[:i] + JS + '\n' + s[i:]

    open(f, 'w', encoding='utf-8', newline='\n').write(s)
    done.append(f)

print('patched %d | already had it %d | problems %d' % (len(done), len(skipped), len(problems)))
if skipped:   print('  skipped:', skipped[:4], '...' if len(skipped) > 4 else '')
if problems:  print('  PROBLEMS:', problems[:6])
