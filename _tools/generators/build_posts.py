# -*- coding: utf-8 -*-
"""Rebuild every post in blog/ on the one-partner.html template.

Retained verbatim from each source file: <title>, meta description, canonical,
published date, the featured image, and the whole <div class="post-content">
block (extracted by brace-matching, not a lazy regex, so nested <div>s survive).
"""
import os, re, sys, html, math, time

SITE  = os.path.expanduser('~/mnt/public')
BLOG  = os.path.join(SITE, 'blog')
BUILD = os.path.expanduser('~/ocblog')
MON   = ['January','February','March','April','May','June','July','August','September','October','November','December']
ABBR  = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

def rd(p): return open(p, encoding='utf-8', errors='replace').read()
def attr(s): return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')

def post_content(s):
    """The post-content div, matched by depth so nested divs are kept."""
    k = s.find('<div class="post-content">')
    if k < 0: return None
    depth = 0
    for m in re.finditer(r'<div\b[^>]*>|</div\s*>', s[k:]):
        depth += -1 if m.group(0).startswith('</') else 1
        if depth == 0:
            return s[k:k + m.end()]
    return None

STOP = set("""a about after all also an and any are as at be been but by can could did do does for from
had has have how i if in into is it its just like made make may more most no not of on one only or other
our out over own said same should so some such than that the their them then there these they this those
to too two up use used using very was way we were what when where which while who why will with would you
your business businesses need needs get gets got new best top guide tips why how what does using online""".split())

def tokens(txt):
    t = re.sub(r'[^a-z0-9 ]', ' ', html.unescape(txt).lower())
    return [w for w in t.split() if len(w) > 2 and w not in STOP]

# ------------------------------------------------------------------ index
posts = []
for f in sorted(os.listdir(BLOG)):
    if not f.endswith('.html'): continue
    s = rd(os.path.join(BLOG, f))
    mt = re.search(r'<title>(.*?)</title>', s, re.S)
    mx = re.search(r'<meta\s+name="description"\s+content="(.*?)"\s*>', s, re.S)
    mc = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"\s*>', s, re.S)
    md = (re.search(r'Published:\s*([0-9]{4})-([0-9]{2})-([0-9]{2})', s) or
          re.search(r'"datePublished":\s*"([0-9]{4})-([0-9]{2})-([0-9]{2})"', s))
    mi = (re.search(r'<figure class="featured-image">\s*<img src="([^"]+)"', s) or
          re.search(r'"(?:\.\./)?featured-images/(?:thumb/)?([^"/]+)"', s))
    pc = post_content(s)
    if not (mt and mx and mc and md and mi and pc):
        print('!! SKIP', f, [n for n, v in
              [('title',mt),('desc',mx),('canonical',mc),('date',md),('image',mi),('post-content',pc)] if not v])
        continue
    title = mt.group(1).strip()
    y, mo, d = int(md.group(1)), int(md.group(2)), int(md.group(3))
    imgbase = os.path.basename(mi.group(1))
    plain = re.sub(r'\s+', ' ', html.unescape(mx.group(1))).strip()
    plain = re.sub(r'\s*\[?\s*…\s*\]?$', '', plain).strip()
    ex = plain if len(plain) <= 138 else plain[:138].rsplit(' ', 1)[0].rstrip(' ,.;:—-') + '…'
    posts.append({
        'file': f, 'title': title, 'desc': mx.group(1).strip(), 'canon': mc.group(1).strip(),
        'date': '%04d-%02d-%02d' % (y, mo, d), 'long': '%d %s %d' % (d, MON[mo-1], y),
        'chip': '%d %s %d' % (d, ABBR[mo-1], y), 'img': imgbase,
        'thumb': os.path.splitext(imgbase)[0] + '.webp',
        'pc': pc, 'plain': plain, 'ex': ex,
        'tok': tokens(title + ' ' + title + ' ' + plain),
    })
print('indexed', len(posts), 'posts')

# ------------------------------------------------------------------ related
N = len(posts)
df = {}
for p in posts:
    for w in set(p['tok']): df[w] = df.get(w, 0) + 1
idf = {w: math.log(N / (1.0 + c)) for w, c in df.items()}
for p in posts:
    v = {}
    for w in p['tok']: v[w] = v.get(w, 0) + 1
    norm = math.sqrt(sum((c * idf[w]) ** 2 for w, c in v.items())) or 1.0
    p['vec'] = {w: c * idf[w] / norm for w, c in v.items()}

for p in posts:
    scored = []
    for q in posts:
        if q['file'] == p['file']: continue
        sml = sum(w * q['vec'][t] for t, w in p['vec'].items() if t in q['vec'])
        # gentle nudge towards posts published near this one, to break ties
        gap = abs(int(p['date'][:4]) - int(q['date'][:4]))
        scored.append((sml - gap * 0.002, q))
    scored.sort(key=lambda x: (-x[0], x[1]['date']))
    p['related'] = [q for _, q in scored[:3]]

# ------------------------------------------------------------------ build
TPL     = rd(os.path.join(SITE, 'one-partner.html'))
TPL     = re.sub(r'(href|src)="(?!https?:|//|/|#|mailto:|tel:|data:|\.\./)([^"]+)"', r'\1="../\2"', TPL)
TPL     = TPL.replace('href="/blog/"', 'href="../blog.html"').replace('href="blog.html"', 'href="../blog.html"')
CSS     = rd(os.path.join(BUILD, 'post_css.txt')) + rd(os.path.join(BUILD, 'rel_css.txt'))
MAIN    = rd(os.path.join(BUILD, 'post_main.txt'))
RELMAIN = rd(os.path.join(BUILD, 'rel_main.txt'))
STY     = TPL.index('</style>')
MA      = TPL.index('<main id="main">')
MB      = TPL.index('</main>') + len('</main>')
HEAD    = TPL[:STY] + CSS + TPL[STY:MA]
TAIL    = TPL[MB:]
from PIL import Image

lo = int(sys.argv[1]) if len(sys.argv) > 1 else 0
hi = int(sys.argv[2]) if len(sys.argv) > 2 else N
t0 = time.time(); wrote = 0

for p in posts[lo:hi]:
    title, desc = p['title'], p['desc']
    W, H = Image.open(os.path.join(BLOG, 'featured-images', p['img'])).size

    head = HEAD
    head = re.sub(r'<title>.*?</title>', lambda _: '<title>' + title + '</title>', head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?">',
                  lambda _: '<meta name="description" content="' + desc + '">', head, count=1, flags=re.S)
    head = re.sub(r'<link rel="canonical" href=".*?">',
                  lambda _: '<link rel="canonical" href="' + p['canon'] + '">', head, count=1, flags=re.S)
    head = re.sub(r'<meta property="og:title" content=".*?">',
                  lambda _: '<meta property="og:title" content="' + title + ' | Online Consulting">', head, count=1, flags=re.S)
    ogd = attr(p['ex'])
    head = re.sub(r'<meta property="og:description" content=".*?">',
                  lambda _: '<meta property="og:description" content="' + ogd + '">', head, count=1, flags=re.S)
    head = re.sub(r'<meta property="og:type" content=".*?">',
                  '<meta property="og:type" content="article">', head, count=1, flags=re.S)
    ld = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "%s",
  "description": "%s",
  "image": "https://onlineconsulting.com.au/blog/featured-images/%s",
  "datePublished": "%s",
  "dateModified": "%s",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "%s" },
  "author": { "@type": "Organization", "name": "Online Consulting" },
  "publisher": {
    "@type": "Organization",
    "name": "Online Consulting",
    "url": "https://onlineconsulting.com.au/",
    "logo": { "@type": "ImageObject", "url": "https://onlineconsulting.com.au/images/OC-Logo.png" }
  }
}
</script>''' % (html.unescape(title).replace('"', '\\"'), p['plain'].replace('"', '\\"'),
                p['img'], p['date'], p['date'], p['canon'])
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: ld, head, count=1, flags=re.S)

    cards = []
    for q in p['related']:
        cards.append(
'      <article class="bl-card" data-reveal>\n'
'        <a class="bl-card__media" href="%s" tabindex="-1" aria-hidden="true">\n'
'          <span class="bl-card__date">%s</span>\n'
'          <img src="featured-images/thumb/%s" alt="" width="860" height="538" loading="lazy" decoding="async">\n'
'        </a>\n'
'        <h3><a href="%s">%s</a></h3>\n'
'        <p>%s</p>\n'
'        <span class="bl-card__rule" aria-hidden="true"></span>\n'
'      </article>' % (q['file'], q['chip'], q['thumb'], q['file'], q['title'], q['ex']))
    rel = RELMAIN.replace('__RELCARDS__', '\n'.join(cards))

    main = (MAIN.replace('__TITLE__', title)
                .replace('__DATELONG__', p['long'])
                .replace('__IMG__', p['img'])
                .replace('__IMGW__', str(W)).replace('__IMGH__', str(H))
                .replace('__POSTCONTENT__', p['pc'])
                .replace('__RELATED__', rel.strip()))

    out = head + main.strip() + TAIL
    assert p['pc'] in out, 'post-content lost: ' + p['file']
    open(os.path.join(BLOG, p['file']), 'w', encoding='utf-8', newline='\n').write(out)
    wrote += 1

print('wrote %d posts (%d..%d) in %.1fs' % (wrote, lo, hi, time.time() - t0))
