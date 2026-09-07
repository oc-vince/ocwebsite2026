# -*- coding: utf-8 -*-
"""Rewrite internal clean URLs back to the real .html file paths.

Local navigation needs the actual files; the live server 301s .html -> clean URL,
so canonical / og:url / JSON-LD / sitemap keep the clean form and are left alone.
"""
import os, re, sys, json

ROOT = os.path.expanduser('~/mnt/public')
DRY  = '--apply' not in sys.argv

# ---- build clean-URL -> real-file map from what is actually on disk ----
pages = {}
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('_tools', '.git', 'dump')]
    for f in fn:
        if not f.endswith('.html'):
            continue
        rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, '/')
        if rel == 'index.html':
            clean = '/'
        elif rel.endswith('/index.html'):
            clean = '/' + rel[:-len('index.html')]
        else:
            clean = '/' + rel[:-5] + '/'
        pages[clean] = '/' + rel

# a couple of legacy links on the old site dropped the /blog/ prefix
EXTRA = {}
for clean, real in list(pages.items()):
    if clean.startswith('/blog/') and clean != '/blog/':
        EXTRA['/' + clean.split('/blog/', 1)[1]] = real
for k, v in EXTRA.items():
    pages.setdefault(k, v)

# nav labels that never had a page - these hrefs get dropped, not remapped
DEAD = {'/managed-it-services/', '/digital-marketing/'}

ATTR = re.compile(r'\bhref="(?P<v>[^"]*)"')
SKIP = re.compile(r'^(?:https?:|//|mailto:|tel:|data:|javascript:|#|$)', re.I)
ASSET = re.compile(r'\.[a-z0-9]{2,5}$', re.I)

# lines we must not touch: canonical, og:url, twitter:url, JSON-LD
GUARD = re.compile(r'rel="canonical"|property="og:url"|name="twitter:url"|application/ld\+json')

def remap(v):
    """clean URL -> real file path, keeping any #frag or ?query"""
    m = re.match(r'^([^#?]*)([#?].*)?$', v, re.S)
    path, tail = m.group(1), (m.group(2) or '')
    if not path.startswith('/'):
        return None
    if path in DEAD:
        return None
    if not path.endswith('/'):
        path += '/'
    real = pages.get(path)
    if real is None:
        return None
    return real + tail

files = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('_tools', '.git', 'dump')]
    for f in fn:
        if f.endswith('.html'):
            files.append(os.path.join(dp, f))
files.sort()

changed = 0; nlinks = 0; unresolved = {}; samples = []
for p in files:
    rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
    s = open(p, encoding='utf-8').read()
    out = []
    pos = 0
    for m in ATTR.finditer(s):
        v = m.group('v')
        out.append(s[pos:m.start()]); pos = m.end()
        keep = m.group(0)
        if SKIP.match(v) or not v.startswith('/'):
            out.append(keep); continue
        bare = re.sub(r'[#?].*$', '', v)
        if ASSET.search(bare):          # /images/x.png, /archives/*.pdf, already-.html
            out.append(keep); continue
        # never rewrite inside a canonical / og:url / JSON-LD context
        ctx = s[max(0, m.start()-260):m.start()]
        if GUARD.search(ctx.split('<')[-1] if '<' in ctx else ctx) or GUARD.search(ctx[-160:]):
            out.append(keep); continue
        new = remap(v)
        if new is None:
            unresolved.setdefault(v, set()).add(rel)
            out.append(keep); continue
        if new == v:
            out.append(keep); continue
        nlinks += 1
        if len(samples) < 12:
            samples.append('%s : %s -> %s' % (rel, v, new))
        out.append('href="%s"' % new)
    out.append(s[pos:])
    n = ''.join(out)
    if n != s:
        changed += 1
        if not DRY:
            open(p, 'w', encoding='utf-8', newline='').write(n)

print('%s files=%d changed=%d links=%d' % ('DRY RUN' if DRY else 'APPLIED', len(files), changed, nlinks))
print('\nsamples:')
for x in samples: print('  ', x)
print('\nleft alone / unresolved (%d distinct):' % len(unresolved))
for v in sorted(unresolved):
    print('   %-58s  in %d file(s)' % (v, len(unresolved[v])))
