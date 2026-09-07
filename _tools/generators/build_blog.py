# -*- coding: utf-8 -*-
import os, re, glob, html

SITE  = os.path.expanduser('~/mnt/Version 2')
BUILD = os.path.expanduser('~/ocblog')
OUT   = os.path.join(SITE, 'blog.html')
MON   = ['January','February','March','April','May','June','July','August','September','October','November','December']
ABBR  = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

def rd(p): return open(p, encoding='utf-8').read()
def attr(s): return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')

# ---------- 1. index every post ----------
posts = []
for f in sorted(glob.glob(os.path.join(SITE, 'blog', '*.html'))):
    s = rd(f)
    mt = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    md = re.search(r'Published:\s*([0-9]{4})-([0-9]{2})-([0-9]{2})', s) or \
         re.search(r'"datePublished":\s*"([0-9]{4})-([0-9]{2})-([0-9]{2})"', s)
    mi = re.search(r'featured-images/(?:thumb/)?([^"/]+)"', s) or \
         re.search(r'<figure class="featured-image">\s*<img src="([^"]+)"', s)
    mx = re.search(r'<meta\s+name="description"\s+content="(.*?)"\s*>', s, re.S)
    if not (mt and md and mi and mx):
        print('SKIP (unparsed):', os.path.basename(f)); continue
    title = re.sub(r'<[^>]+>', '', mt.group(1)).strip()
    y, m, d = int(md.group(1)), int(md.group(2)), int(md.group(3))
    img = os.path.splitext(os.path.basename(mi.group(1)))[0] + '.webp'
    plain = re.sub(r'\s+', ' ', html.unescape(mx.group(1))).strip()
    plain = re.sub(r'\s*\[?…\]?$|\s*\[\s*&?hellip;?\s*\]$', '', plain).strip()
    ex = plain if len(plain) <= 138 else plain[:138].rsplit(' ', 1)[0].rstrip(' ,.;:—-') + '…'
    posts.append({
        'file' : os.path.basename(f),
        'title': title,
        'sort' : '%04d-%02d-%02d' % (y, m, d),
        'long' : '%d %s %d' % (d, MON[m-1], y),
        'chip' : '%d %s %d' % (d, ABBR[m-1], y),
        'img'  : img,
        'ex'   : ex,
        'plain': plain,
    })

posts.sort(key=lambda p: (p['sort'], p['file']), reverse=True)
missing = [p['img'] for p in posts if not os.path.exists(os.path.join(SITE, 'blog', 'featured-images', 'thumb', p['img']))]
print('posts:', len(posts), '| thumbs missing:', len(missing), missing[:5])

# ---------- 2. cards ----------
feat, rest = posts[0], posts[1:]
cards = []
for p in rest:
    href = 'blog/' + p['file']
    idx  = attr(html.unescape(p['title'] + ' ' + p['plain']).lower())
    cards.append(
'      <article class="bl-card" data-t="%s">\n'
'        <a class="bl-card__media" href="%s" tabindex="-1" aria-hidden="true">\n'
'          <span class="bl-card__date">%s</span>\n'
'          <img src="blog/featured-images/thumb/%s" alt="" width="860" height="538" loading="lazy" decoding="async">\n'
'        </a>\n'
'        <h3><a href="%s">%s</a></h3>\n'
'        <p>%s</p>\n'
'        <span class="bl-card__rule" aria-hidden="true"></span>\n'
'      </article>' % (idx, href, p['chip'], p['img'], href, p['title'], attr(p['ex']).replace('&quot;', '"')))

# ---------- 3. template ----------
tpl = rd(os.path.join(SITE, 'one-partner.html'))
tpl = tpl.replace('href="/blog/"', 'href="blog.html"')

TITLE = 'Blog | IT, Web &amp; Digital Marketing Insights | Online Consulting'
DESC  = ('Practical articles from the Online Consulting team on managed IT support, cyber security, '
         'web design, hosting and digital marketing for Australian businesses.')
tpl = re.sub(r'<title>.*?</title>', lambda _: '<title>' + TITLE + '</title>', tpl, count=1, flags=re.S)
tpl = re.sub(r'<meta name="description" content=".*?">',
             lambda _: '<meta name="description" content="' + DESC + '">', tpl, count=1, flags=re.S)
tpl = re.sub(r'<link rel="canonical" href=".*?">',
             '<link rel="canonical" href="https://onlineconsulting.com.au/blog/">', tpl, count=1, flags=re.S)
tpl = re.sub(r'<meta property="og:title" content=".*?">',
             '<meta property="og:title" content="Blog | Online Consulting">', tpl, count=1, flags=re.S)
tpl = re.sub(r'<meta property="og:description" content=".*?">',
             lambda _: '<meta property="og:description" content="' + DESC + '">', tpl, count=1, flags=re.S)

items = '\n'.join(
    '    { "@type": "ListItem", "position": %d, "url": "https://onlineconsulting.com.au/blog/%s", "name": "%s" }%s'
    % (i + 1, p['file'], html.unescape(p['title']).replace('"', '\\"'), ',' if i < 9 else '')
    for i, p in enumerate(posts[:10]))
ld = ('<script type="application/ld+json">\n{\n'
      '  "@context": "https://schema.org",\n  "@type": "Blog",\n'
      '  "name": "Online Consulting Blog",\n'
      '  "url": "https://onlineconsulting.com.au/blog/",\n'
      '  "description": "%s",\n'
      '  "publisher": { "@type": "Organization", "name": "Online Consulting", "url": "https://onlineconsulting.com.au/" },\n'
      '  "blogPost": [\n%s\n  ]\n}\n</script>' % (DESC, items))
tpl = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: ld, tpl, count=1, flags=re.S)

css = rd(os.path.join(BUILD, 'blog_css.txt'))
i = tpl.index('</style>')
tpl = tpl[:i] + css + tpl[i:]

main = rd(os.path.join(BUILD, 'blog_main.txt'))
main = (main.replace('__F_HREF__', 'blog/' + feat['file'])
            .replace('__F_IMG__', 'blog/featured-images/thumb/' + feat['img'])
            .replace('__F_ALT__', attr(feat['title']))
            .replace('__F_TITLE__', feat['title'])
            .replace('__F_EXCERPT__', feat['ex'])
            .replace('__F_DATE__', feat['long'])
            .replace('__TOTAL__', str(len(rest)))
            .replace('__CARDS__', '\n'.join(cards)))
a = tpl.index('<main id="main">')
b = tpl.index('</main>') + len('</main>')
tpl = tpl[:a] + main.strip() + tpl[b:]

open(OUT, 'w', encoding='utf-8', newline='\n').write(tpl)
print('wrote', OUT, len(tpl), 'bytes | featured:', feat['sort'], feat['title'][:60])
