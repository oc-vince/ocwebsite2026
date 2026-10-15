# -*- coding: utf-8 -*-
import os
ROOT = os.path.expanduser('~/mnt/public')
# Every post is a folder with an index.html, so the slug is the folder name.
slugs = sorted(d for d in os.listdir(os.path.join(ROOT, 'blog'))
               if os.path.isdir(os.path.join(ROOT, 'blog', d))
               and os.path.exists(os.path.join(ROOT, 'blog', d, 'index.html')))

L = []
def sec(t): L.append(''); L.append('# ' + t)

L.append('# Online Consulting - Netlify redirects')
L.append('# Generated for the 2026 rebuild. First matching rule wins, so order matters.')
L.append('#')
L.append('# Every page is a folder with an index.html, so its canonical URL ends in a')
L.append('# trailing slash and the server needs no rewrite to produce one. The legacy')
L.append('# .html paths 301 to that URL. The ! flag forces a redirect even when a file')
L.append('# matches. Trailing slashes are normalised before these rules run: a rule')
L.append('# written /foo also matches /foo/.')

sec('Build tooling lives in the repo but must not be served')
L.append('/_tools/*                                 /_not-found                  404')

# ---- clean URLs, generated from what is actually on disk ----
pages = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('_tools', '.git', 'dump')]
    if 'index.html' not in fn:
        continue
    rel = os.path.relpath(dp, ROOT).replace(os.sep, '/')
    pages.append('/' if rel == '.' else '/' + rel + '/')
pages.sort()

sec('Legacy .html paths 301 to the folder URL the page now lives at')
L.append('# The pages used to be flat .html files; they are folders now. These cover any')
L.append('# bookmark, backlink or old internal link still pointing at the file path.')
L.append('# / is deliberately absent: a forced rule on /index.html can loop, and Netlify')
L.append('# already 301s /index.html -> / on its own.')
for c in pages:
    if c == '/':
        continue
    stem = c[:-1]                      # /about/ -> /about
    L.append('%-78s %-78s 301!' % (stem + '.html', c))
    L.append('%-78s %-78s 301!' % (c + 'index.html', c))

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
# the three shop URLs go to the homepage per the 301 mapping sheet; the rest
# keep the contact page, which the sheet does not cover
for p in ['buy-now', 'buy-now-it', 'buy-services']:
    L.append('/%-40s /  301' % p)
for p in ['my-account', 'dashboard', 'user-hosting', 'update-detail',
          'development-and-support']:
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


# ---- rows from "Blog Post Meta Tags.xlsx" / 301 mapping that are not already
# covered above. Skipped deliberately:
#   * "No change" rows - nothing to redirect
#   * /service/google-adwords/ -> /service/google-ads/ : the target page does
#     not exist, and the source is a live page, so the rule would 301 the
#     Google Ads page to a 404
#   * query-string variants (/buy-now/?plan=...) - a source without a query
#     already matches the request whatever its query string
#   * /about/ -> /about and /work/ -> /work : the same page either way, since
#     trailing slashes are normalised before rules run
# Destinations are normalised to end in a trailing slash, because that is the
# canonical form of every page on this site.
import json as _json
_sheet = os.path.join(ROOT, '_tools/content-2026-09/redirects_sheet.json')
if os.path.exists(_sheet):
    _rows = _json.load(open(_sheet, encoding='utf-8'))
    _have = set()
    for _l in L:
        if _l and not _l.startswith('#'):
            _have.add(_l.split()[0].rstrip('/') or '/')
    _SKIP = {'/service/google-adwords/'}
    _norm = lambda x: (x.rstrip('/') or '/')

    def _slash(u):
        # every page on this site lives at a folder URL, so a destination ends
        # in '/' - before any #anchor, and never for an off-site or file target
        if u.startswith('http') or '.' in u.rsplit('/', 1)[-1]:
            return u
        _p, _h, _a = u.partition('#')
        if not _p.endswith('/'):
            _p += '/'
        return _p + _h + _a
    _extra = []
    for _r in _rows:
        _o, _n = _r['Old'] if 'Old' in _r else _r['old'], _r['new']
        if _n.lower() == 'no change' or _o in _SKIP or '?' in _o:
            continue
        if _norm(_o) == _norm(_n):
            continue
        if _norm(_o) in _have:
            continue
        _extra.append('%-56s %-46s 301' % (_o, _slash(_n)))
        _have.add(_norm(_o))
    if _extra:
        # These must sit BEFORE the /work/:slug, /team/:slug, /speciality/:slug
        # and /testimonial/:slug wildcards. First match wins, so appending them
        # at the end would let the wildcards swallow every one of them - and the
        # sheet sends several of those slugs somewhere different from the
        # wildcard (team members to a #bio anchor, testimonials to /).
        _block = ['', '# From the 301 mapping sheet',
                  '# Ahead of the :slug wildcards below, which would otherwise match first.']
        _block += sorted(_extra)
        try:
            _at = L.index('# Sections the new site rolls up into one page') - 1
        except ValueError:
            _at = len(L)
        L[_at:_at] = _block

open(os.path.join(ROOT, '_redirects'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('rules:', sum(1 for x in L if x and not x.startswith('#')))
print('lines:', len(L))
