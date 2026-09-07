import os, glob, re
ROOT = os.path.expanduser('~/mnt/public')
MAP = {
 '/digital-marketing/seo/':                ('service/seo-services/index.html',            '../seo-services/index.html'),
 '/digital-marketing/google-ads/':         ('service/google-adwords/index.html',          '../google-adwords/index.html'),
 '/digital-marketing/social-media/':       ('service/social-media-marketing/index.html',  '../social-media-marketing/index.html'),
 '/digital-marketing/content-copywriting/':('service/copywriting/index.html',             '../copywriting/index.html'),
 '/about/':                                ('about.html',                                 '../../about.html'),
}
files = sorted(glob.glob(os.path.join(ROOT,'*.html')) + glob.glob(os.path.join(ROOT,'service','*','index.html')))
for f in files:
    depth = 1 if os.path.dirname(f) == ROOT else 2
    s = open(f, encoding='utf-8').read(); orig = s; n = 0
    for old,(root_t, svc_t) in MAP.items():
        new = root_t if depth == 1 else svc_t
        c = s.count('href="%s"' % old)
        if c: n += c; s = s.replace('href="%s"' % old, 'href="%s"' % new)
    if s != orig:
        open(f,'w',encoding='utf-8',newline='\n').write(s)
        print('%-46s %3d links' % (os.path.relpath(f, ROOT), n))
