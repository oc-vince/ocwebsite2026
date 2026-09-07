# -*- coding: utf-8 -*-
"""Rewrite every internal href/src/data-shot to a root-relative clean URL.

Runs in two phases:
  1. rewrite links in place, using each file's CURRENT location to resolve ../
  2. move blog.html / book.html / contact.html into their same-named folders as
     index.html, which removes the /blog/ vs blog/ ambiguity. Safe only after
     phase 1, because the rewritten paths no longer depend on file depth.
"""
import os, re, sys, shutil

ROOT   = os.path.expanduser('~/mnt/Version 2')
DOMAIN = 'https://onlineconsulting.com.au'
DRY    = '--apply' not in sys.argv

ATTR = re.compile(r'(?P<a>href|src|data-shot)="(?P<v>[^"]*)"')
SKIP = re.compile(r'^(?:https?:|//|mailto:|tel:|data:|javascript:|#|$)', re.I)

def clean(path_from_root):
    """'service/x/index.html' -> '/service/x/' ; 'blog/y.html' -> '/blog/y/'"""
    m = re.match(r'^([^#?]*)(.*)$', path_from_root, re.S)
    path, tail = m.group(1), m.group(2)
    if path == 'index.html':
        out = '/'
    elif path.endswith('/index.html'):
        out = '/' + path[:-len('index.html')]
    elif path.endswith('.html'):
        out = '/' + path[:-5] + '/'
    else:
        out = '/' + path
    return out + tail

def canonical_for(relpath):
    return DOMAIN + clean(relpath.replace(os.sep, '/'))

files = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d != 'dump']
    for f in fn:
        if f.endswith('.html'):
            files.append(os.path.join(dp, f))
files.sort()

changed = 0; nlinks = 0; ncanon = 0; samples = []; escapes = []
for p in files:
    rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
    d   = os.path.dirname(rel)
    s   = open(p, encoding='utf-8').read()
    o   = s

    def sub(m):
        global nlinks
        a, v = m.group('a'), m.group('v')
        if SKIP.match(v):
            return m.group(0)
        if v.startswith('/'):
            target = v.lstrip('/')
        else:
            target = os.path.normpath(os.path.join(d, v)).replace(os.sep, '/') if d else v
            target = re.sub(r'^\./', '', target)
        if target.startswith('..'):
            escapes.append((rel, v))
            return m.group(0)
        # normpath eats the #frag, so re-attach it from the original value
        frag = re.search(r'([#?].*)$', v, re.S)
        if frag:
            target = re.sub(r'[#?].*$', '', target) + frag.group(1)
        new = clean(target)
        if new == v:
            return m.group(0)
        nlinks += 1
        if len(samples) < 14:
            samples.append('%s : %s -> %s' % (rel, v, new))
        return '%s="%s"' % (a, new)

    s = ATTR.sub(sub, s)

    # canonical must point at this page's own new URL, not the old live one
    want = canonical_for(rel)
    s, k = re.subn(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + want + m.group(2), s)
    if k:
        ncanon += k

    if s != o:
        changed += 1
        if not DRY:
            open(p, 'w', encoding='utf-8', newline='').write(s)

print('%s  files=%d changed=%d links=%d canonical=%d' % ('DRY RUN' if DRY else 'APPLIED', len(files), changed, nlinks, ncanon))
print('\nsample rewrites:')
for x in samples: print('  ', x)
if escapes:
    print('\nWARNING refs that escape the site root (%d):' % len(escapes))
    for x in escapes[:10]: print('  ', x)

if not DRY:
    for name in ('blog', 'book', 'contact'):
        src = os.path.join(ROOT, name + '.html')
        dst = os.path.join(ROOT, name, 'index.html')
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            print('moved %s.html -> %s/index.html' % (name, name))
