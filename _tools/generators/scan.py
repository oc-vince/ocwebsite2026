import os,re,json,urllib.parse
MEDIA={'.jpg','.jpeg','.png','.gif','.webp','.svg','.ico','.avif','.bmp','.tif','.tiff','.mp4','.webm','.mov','.m4v','.ogv','.avi','.mkv'}
EXT='|'.join(e[1:] for e in MEDIA)
media=[];htmls=[]
for dp,dn,fn in os.walk('.'):
    dn[:]=[d for d in dn if d!='dump' and not d.startswith('.')]
    for f in fn:
        p=os.path.normpath(os.path.join(dp,f)).replace(os.sep,'/'); e=os.path.splitext(f)[1].lower()
        if e in MEDIA: media.append(p)
        elif e in ('.html','.htm'): htmls.append(p)
mset={p.lower() for p in media}

pat=re.compile(r'[A-Za-z0-9_%~.\-/]+\.(?:'+EXT+r')\b', re.I)
strong=set(); weak={}
for h in htmls:
    d=os.path.dirname(h)
    for m in pat.finditer(open(h,encoding='utf-8',errors='replace').read()):
        tok=urllib.parse.unquote(m.group(0))
        if '/' in tok:
            cand = tok.lstrip('/') if tok.startswith('/') else os.path.normpath(os.path.join(d,tok))
            cand = os.path.normpath(cand).replace(os.sep,'/').lstrip('./')
            if cand.lower() in mset: strong.add(cand.lower()); continue
        weak.setdefault(os.path.basename(tok).lower(), set()).add(h)

used=set(strong)
weakhits={}
for p in media:
    b=os.path.basename(p).lower()
    if p.lower() in used: continue
    if b in weak:
        used.add(p.lower()); weakhits.setdefault(b,[]).append(p)
unused=sorted(p for p in media if p.lower() not in used)
json.dump(unused, open(os.path.expanduser('~/ocblog/unused.json'),'w'))
print('media %d | resolved refs %d | kept %d | unused %d'%(len(media),len(strong),len(media)-len(unused),len(unused)))
print('unused size: %.1f MB'%(sum(os.path.getsize(p) for p in unused)/1048576))
print('\nkept only by loose name match (no resolvable path) — review:')
for b,ps in sorted(weakhits.items()):
    print('   %-42s -> %s  (named in %s)'%(b, ps, sorted(weak[b])[:2]))
