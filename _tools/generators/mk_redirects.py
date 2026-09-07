# -*- coding: utf-8 -*-
import os
ROOT = os.path.expanduser('~/mnt/public')
slugs = sorted(f[:-5] for f in os.listdir(os.path.join(ROOT, 'blog'))
                if f.endswith('.html') and f != 'index.html')  # index.html is the blog listing, not a post

L = []
def sec(t): L.append(''); L.append('# ' + t)

L.append('# Online Consulting - Netlify redirects')
L.append('# Generated for the 2026 rebuild. First matching rule wins, so order matters.')
L.append('#')
L.append('# Every page ships as a real .html file so the site can be browsed straight')
L.append('# from disk on a local server. On the live server the .html paths 301 to the')
L.append('# clean URL, so only the clean URL is ever visible or indexed.')
L.append('# Trailing slashes are normalised before these rules run: a rule written /foo')
L.append('# also matches /foo/. The ! flag forces a redirect even when a file matches.')

sec('Build tooling lives in the repo but must not be served')
L.append('/_tools/*                                 /_not-found                  404')

# ---- .html <-> clean URL, generated from what is actually on disk ----
htmls = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('_tools', '.git', 'dump')]
    for f in fn:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, '/')
            if rel == '404.html':
                continue   # Netlify serves this internally; it has no clean URL
            htmls.append(rel)
htmls.sort()

def clean_of(rel):
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]
    return '/' + rel[:-5] + '/'

sec('Canonical URLs: the .html file the local server uses 301s to the clean URL')
L.append('# /index.html is deliberately absent: a forced rule on it can loop, and Netlify')
L.append('# already 301s /index.html -> / on its own.')
for rel in htmls:
    if rel == 'index.html':
        continue
    L.append('/%-78s %-78s 301!' % (rel, clean_of(rel)))

sec('And the clean URL serves that same file, without changing the address bar')
L.append('# Netlify Pretty URLs does this on its own; spelled out so the site does not')
L.append('# depend on that setting staying on.')
for rel in htmls:
    c = clean_of(rel)
    if c == '/':
        continue          # / already serves index.html natively
    L.append('%-79s /%-78s 200' % (c, rel))

sec('Blog posts: the old site published these at the root, the new site nests them under /blog/')
for s in slugs:
    L.append('/%-78s /blog/%s/  301' % (s, s))

sec('Nav parents that have no hub page built yet - point them at the lead service')
L.append('# TODO replace these two with real hub pages; the top nav links here on every page')
L.append('/managed-it-services                      /service/it-support/        301')
L.append('/digital-marketing                        /service/seo-services/      301')

sec('Service pages whose slug changed')
L.append('/service/google-workspace-microsoft-365   /service/google-workspace/  301')
L.append('/service/search-engine-marketing          /service/seo-services/      301')

sec('Standalone pages that are now service pages')
L.append('/video                                    /service/video/             301')
L.append('/photography                              /service/photography/       301')
L.append('/google-workspace                         /service/google-workspace/  301')

sec('Northern Beaches landing pages -> closest service page')
L.append('/seo-northern-beaches                                     /service/seo-services/      301')
L.append('/search-engine-marketing-seo-and-adwords-expert-northern-beaches  /service/seo-services/  301')
L.append('/web-design-and-web-development-northern-beaches          /service/web-development/   301')
L.append('/video-producer-and-photography-northern-beaches           /service/video/             301')
L.append('/onsite-computer-repairs-and-fix-northern-beaches          /service/computer-repairs/  301')
L.append('/it-help-and-computer-geek-northern-beaches                /service/computer-repairs/  301')

sec('Retired customer portal and WooCommerce pages')
for p in ['buy-now', 'buy-now-it', 'buy-services', 'my-account', 'dashboard',
          'user-hosting', 'update-detail', 'development-and-support']:
    L.append('/%-40s /contact/  301' % p)

sec('COVID-era content')
L.append('/covid-19-key-information                 /                           301')
L.append('/covid/:slug                              /                           301')

sec('Sections the new site rolls up into one page')
L.append('# :slug never matches an empty segment, so /work/ and /people/ themselves are safe')
L.append('/work/:slug                               /work/                      301')
L.append('/team/:slug                               /people/                    301')
L.append('/speciality/:slug                         /one-partner/               301')
L.append('/testimonial/:slug                        /work/                      301')

open(os.path.join(ROOT, '_redirects'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('rules:', sum(1 for x in L if x and not x.startswith('#')))
print('lines:', len(L))
