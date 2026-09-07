# -*- coding: utf-8 -*-
import os
ROOT = os.path.expanduser('~/mnt/Version 2')
slugs = sorted(f[:-5] for f in os.listdir(os.path.join(ROOT, 'blog'))
                if f.endswith('.html') and f != 'index.html')  # index.html is the blog listing, not a post

L = []
def sec(t): L.append(''); L.append('# ' + t)

L.append('# Online Consulting - Netlify redirects')
L.append('# Generated for the 2026 rebuild. First matching rule wins, so order matters.')
L.append('#')
L.append('# Netlify "Pretty URLs" (on by default) already serves about.html at /about/ and')
L.append('# 301s /about.html -> /about/, so .html -> clean-URL rules are NOT listed here.')
L.append('# Trailing slashes are normalised before these rules run: a rule written /foo')
L.append('# also matches /foo/. The ! flag forces a redirect even when a file matches.')

sec('Build tooling lives in the repo but must not be served')
L.append('/_tools/*                                 /_not-found                  404')

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
