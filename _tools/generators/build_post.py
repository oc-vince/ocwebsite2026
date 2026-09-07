# -*- coding: utf-8 -*-
import os, re, html
from PIL import Image

SITE = os.path.expanduser('~/mnt/Version 2')
BUILD = os.path.expanduser('~/ocblog')
SLUG = '5-futuristic-technology-trends-in-ecommerce-industry'
SRC = os.path.join(SITE, 'blog', SLUG + '.html')
OUT = SRC

def rd(p):
    return open(p, encoding='utf-8').read()

# ---------- 1. harvest from the original export ----------
orig = rd(SRC)
title = re.search(r'<title>(.*?)</title>', orig, re.S).group(1).strip()
title = title.split(' | ')[0].strip()
desc  = re.search(r'<meta\s+name="description"\s+content="(.*?)"\s*>', orig, re.S).group(1).strip()
canon = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"\s*>', orig, re.S).group(1).strip()
mdate = re.search(r'Published:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})', orig) or \
        re.search(r'"datePublished":\s*"([0-9]{4}-[0-9]{2}-[0-9]{2})"', orig)
date  = mdate.group(1)
imgsrc = (re.search(r'<figure class="featured-image">\s*<img src="([^"]+)"', orig) or
          re.search(r'"(?:\.\./)?featured-images/([^"]+)"', orig)).group(1)
imgbase = os.path.basename(imgsrc)
pc = re.search(r'<div class="post-content">.*?</div>', orig, re.S).group(0)

MON = ['January','February','March','April','May','June','July','August','September','October','November','December']
y, m, d = [int(x) for x in date.split('-')]
datelong = '%d %s %d' % (d, MON[m-1], y)

imgpath = os.path.join(SITE, 'blog', 'featured-images', imgbase)
assert os.path.exists(imgpath), 'featured image missing: ' + imgbase
W, H = Image.open(imgpath).size

# ---------- 2. take the template and re-base it for /blog/ ----------
tpl = rd(os.path.join(SITE, 'one-partner.html'))
tpl = re.sub(r'(href|src)="(?!https?:|//|/|#|mailto:|tel:|data:|\.\./)([^"]+)"', r'\1="../\2"', tpl)
tpl = tpl.replace('href="/blog/"', 'href="../blog.html"')

# ---------- 3. head ----------
esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;') \
                 .replace('&amp;amp;', '&amp;').replace('&amp;#', '&#').replace('&amp;hellip;', '&hellip;') \
                 .replace('&amp;rsquo;', '&rsquo;').replace('&amp;lsquo;', '&lsquo;') \
                 .replace('&amp;ldquo;', '&ldquo;').replace('&amp;rdquo;', '&rdquo;') \
                 .replace('&amp;nbsp;', '&nbsp;').replace('&amp;mdash;', '&mdash;').replace('&amp;ndash;', '&ndash;')

tpl = re.sub(r'<title>.*?</title>', lambda _: '<title>' + title + '</title>', tpl, count=1, flags=re.S)
tpl = re.sub(r'<meta name="description" content=".*?">',
             lambda _: '<meta name="description" content="' + desc + '">', tpl, count=1, flags=re.S)
tpl = re.sub(r'<link rel="canonical" href=".*?">',
             lambda _: '<link rel="canonical" href="' + canon + '">', tpl, count=1, flags=re.S)
plain = re.sub(r'\s+', ' ', html.unescape(desc)).strip()
short = plain[:180].rsplit(' ', 1)[0].rstrip(' ,.;:') + '…' if len(plain) > 180 else plain
ogd = esc(short)
tpl = re.sub(r'<meta property="og:title" content=".*?">',
             lambda _: '<meta property="og:title" content="' + title + ' | Online Consulting">', tpl, count=1, flags=re.S)
tpl = re.sub(r'<meta property="og:description" content=".*?">',
             lambda _: '<meta property="og:description" content="' + ogd + '">', tpl, count=1, flags=re.S)
tpl = re.sub(r'<meta property="og:type" content=".*?">',
             '<meta property="og:type" content="article">', tpl, count=1, flags=re.S)

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
</script>''' % (html.unescape(title).replace('"', '\\"'), plain.replace('"', '\\"'), imgbase, date, date, canon)
tpl = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: ld, tpl, count=1, flags=re.S)

# ---------- 4. css ----------
css = rd(os.path.join(BUILD, 'post_css.txt'))
i = tpl.index('</style>')
tpl = tpl[:i] + css + tpl[i:]

# ---------- 5. main ----------
main = rd(os.path.join(BUILD, 'post_main.txt'))
main = main.replace('__TITLE__', title).replace('__DATELONG__', datelong)
main = main.replace('__IMG__', imgbase).replace('__IMGW__', str(W)).replace('__IMGH__', str(H))
main = main.replace('__POSTCONTENT__', pc)
a = tpl.index('<main id="main">')
b = tpl.index('</main>') + len('</main>')
tpl = tpl[:a] + main.strip() + tpl[b:]

open(OUT, 'w', encoding='utf-8', newline='\n').write(tpl)
print('wrote', OUT, len(tpl), 'bytes')
print('title:', title)
print('date :', datelong)
print('image:', imgbase, W, 'x', H)
print('post-content preserved byte-for-byte:', pc in tpl, len(pc))
