import re, os, sys, json
ROOT = os.path.expanduser('~/mnt/Version 2')
BUILD = os.path.expanduser('~/oc_build')

def rd(p):
    with open(p, encoding='utf-8') as f: return f.read()

def build(template, out, title, desc, canonical, ogt, ogd, ldjson, css_file, main_file):
    html = rd(os.path.join(ROOT, template))
    # head meta
    html = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content=".*?">',
                  '<meta name="description" content="%s">' % desc, html, count=1, flags=re.S)
    html = re.sub(r'<link rel="canonical" href=".*?">',
                  '<link rel="canonical" href="%s">' % canonical, html, count=1, flags=re.S)
    html = re.sub(r'<meta property="og:title" content=".*?">',
                  '<meta property="og:title" content="%s">' % ogt, html, count=1, flags=re.S)
    html = re.sub(r'<meta property="og:description" content=".*?">',
                  '<meta property="og:description" content="%s">' % ogd, html, count=1, flags=re.S)
    # json-ld
    new_ld = '<script type="application/ld+json">\n' + json.dumps(ldjson, indent=2) + '\n</script>'
    n = len(re.findall(r'<script type="application/ld\+json">.*?</script>', html, flags=re.S))
    assert n >= 1, 'no ld+json in template'
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: new_ld, html, count=1, flags=re.S)
    # extra css before the first </style>
    css = rd(os.path.join(BUILD, css_file))
    i = html.index('</style>')
    html = html[:i] + css + html[i:]
    # main
    main = rd(os.path.join(BUILD, main_file)).rstrip() + '\n'
    a = html.index('<main id="main">')
    b = html.index('</main>') + len('</main>')
    html = html[:a] + main.strip() + html[b:]
    dest = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(dest), exist_ok=True) if os.path.dirname(dest) else None
    with open(dest, 'w', encoding='utf-8', newline='\n') as f: f.write(html)
    print('wrote', out, len(html), 'bytes')
