# -*- coding: utf-8 -*-
"""Fresh sitemap.xml + robots.txt for the clean-URL build."""
import os, re, datetime
ROOT = os.path.expanduser('~/mnt/Version 2')
D = 'https://onlineconsulting.com.au'
os.chdir(ROOT)

def clean(rel):
    if rel == 'index.html': return '/'
    if rel.endswith('/index.html'): return '/' + rel[:-len('index.html')]
    return '/' + rel[:-5] + '/'

pages = []
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d != 'dump']
    for f in fn:
        if not f.endswith('.html'): continue
        rel = os.path.relpath(os.path.join(dp, f), '.').replace(os.sep, '/')
        pages.append(rel)

# thank-you pages are conversion end-points, not search landing pages
pages = [p for p in pages if 'thank-you' not in p]

def prio(u):
    if u == '/': return '1.0', 'weekly'
    if u.startswith('/service/'): return '0.9', 'monthly'
    if u == '/blog/': return '0.8', 'weekly'
    if u.startswith('/blog/'): return '0.6', 'yearly'
    if u in ('/contact/', '/book/'): return '0.8', 'monthly'
    if u == '/privacy-policy/': return '0.2', 'yearly'
    return '0.7', 'monthly'

def lastmod(rel):
    # blog posts carry their own published date in the JSON-LD
    try:
        s = open(rel, encoding='utf-8').read(4000)
        m = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', s)
        if m: return m.group(1)
    except Exception:
        pass
    return datetime.date.today().isoformat()

urls = sorted(((clean(p), p) for p in pages),
              key=lambda x: (x[0] != '/', x[0].startswith('/blog/') and x[0] != '/blog/', x[0]))

out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, rel in urls:
    pr, cf = prio(u)
    out += ['  <url>',
            '    <loc>%s%s</loc>' % (D, u),
            '    <lastmod>%s</lastmod>' % lastmod(rel),
            '    <changefreq>%s</changefreq>' % cf,
            '    <priority>%s</priority>' % pr,
            '  </url>']
out.append('</urlset>')
open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')

open('robots.txt', 'w', encoding='utf-8', newline='\n').write(
    'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % D)

print('sitemap.xml: %d URLs' % len(urls))
print('robots.txt written')
print('\nfirst 10:')
for u, _ in urls[:10]: print('  ', u)
