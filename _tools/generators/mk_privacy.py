# -*- coding: utf-8 -*-
"""Build privacy-policy.html from a blog post skeleton (shared header, nav,
mega menus, mobile menu, footer and scripts), swapping in the policy content."""
import os, re

ROOT = os.path.expanduser('~/mnt/Version 2')
SRC  = os.path.join(ROOT, 'blog', 'how-social-media-helps-with-seo.html')
OUT  = os.path.join(ROOT, 'privacy-policy.html')
BODY = open(os.path.expanduser('~/ocblog/pp_body.html'), encoding='utf-8').read().rstrip('\n')

s = open(SRC, encoding='utf-8').read()

TITLE = 'Privacy Policy | Online Consulting'
DESC  = ('How Online Consulting collects, uses, protects and discloses your personal '
         'information, and how to contact us about privacy. Bound by the Privacy Act 1988 (Cth).')
URL   = 'https://onlineconsulting.com.au/privacy-policy/'

def swap(pattern, repl, why, count=1):
    global s
    s2, n = re.subn(pattern, repl, s, count=count, flags=re.S)
    assert n == count, 'failed: %s (matched %d)' % (why, n)
    s = s2

# ---- head ----
swap(r'<title>.*?</title>', lambda m: '<title>%s</title>' % TITLE, 'title')
swap(r'<meta name="description" content=".*?">',
     lambda m: '<meta name="description" content="%s">' % DESC, 'description')
swap(r'<link rel="canonical" href=".*?">',
     lambda m: '<link rel="canonical" href="%s">' % URL, 'canonical')
swap(r'<meta property="og:title" content=".*?">',
     lambda m: '<meta property="og:title" content="%s">' % TITLE, 'og:title')
swap(r'<meta property="og:description" content=".*?">',
     lambda m: '<meta property="og:description" content="%s">' % DESC, 'og:description')
swap(r'<meta property="og:type" content=".*?">',
     lambda m: '<meta property="og:type" content="website">', 'og:type')

# ---- JSON-LD: BlogPosting -> WebPage ----
LD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Privacy Policy",
  "description": "%s",
  "url": "%s",
  "dateModified": "2026-09-07",
  "inLanguage": "en-AU",
  "isPartOf": { "@type": "WebSite", "name": "Online Consulting", "url": "https://onlineconsulting.com.au/" },
  "publisher": {
    "@type": "Organization",
    "name": "Online Consulting",
    "url": "https://onlineconsulting.com.au/",
    "logo": { "@type": "ImageObject", "url": "https://onlineconsulting.com.au/images/OC-Logo.png" }
  },
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://onlineconsulting.com.au/" },
      { "@type": "ListItem", "position": 2, "name": "Privacy Policy", "item": "%s" }
    ]
  }
}
</script>''' % (DESC, URL, URL)
swap(r'<script type="application/ld\+json">.*?</script>', lambda m: LD, 'json-ld')

# ---- hero ----
HERO = '''<!-- ============ HERO ============ -->
<section class="hero hero--page hero--book hero--blog">
  <div class="container hero__inner">
    <nav class="crumbs" aria-label="Breadcrumb" data-reveal>
      <a href="/">Home</a><i>&rsaquo;</i><span>Privacy Policy</span>
    </nav>
    <h1 class="reveal-lines" id="heroTitle">Privacy Policy</h1>
    <p class="hero__sub" data-reveal>How we collect, use and protect your personal information.</p>
  </div>
</section>

'''
swap(r'<!-- ============ HERO ============ -->.*?(?=<!-- ============ ARTICLE ============ -->)',
     lambda m: HERO, 'hero')

# ---- article: no featured image, no "What's inside" TOC script ----
ART = '''<!-- ============ POLICY ============ -->
<section class="bp">
  <div class="container">
    <div class="bp__article">

%s

    </div>
  </div>
</section>

''' % BODY
swap(r'<!-- ============ ARTICLE ============ -->.*?(?=<!-- ============ RELATED ARTICLES ============ -->)',
     lambda m: ART, 'article')

# ---- drop Related Articles ----
swap(r'<!-- ============ RELATED ARTICLES ============ -->.*?(?=<!-- ============ FOOTER)',
     lambda m: '', 'related')

open(OUT, 'w', encoding='utf-8', newline='').write(s)
print('wrote privacy-policy.html  %d bytes' % len(s))
for probe in ('bp-figure', 'bpToc', 'rel-sec', 'BlogPosting', 'Related Articles'):
    print('  %-18s present: %s' % (probe, probe in s))
