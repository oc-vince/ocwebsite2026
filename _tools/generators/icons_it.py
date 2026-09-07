import os, re
ROOT = os.path.expanduser('~/mnt/public')
MAP = [
 ('IT-Support-in-Sydney-Icon.png',       'IT-Support-in-Sydney.svg',    41, 46),
 ('Managed-Cyber-Security-Icon.png',     'Managed-Cyber-Security.svg',  46, 45),
 ('Managed-Network-Packages-Icon.png',   'Managed-Network.svg',         42, 46),
 ('Robust-Cloud-Backup-Icon.png',        'Robust-Cloud-Backup.svg',     46, 46),
 ('Ongoing-Maintenance-Icon.png',        'Ongoing-Maintenance.svg',     46, 46),
 ('Google-Workspace-Icon.png',           'Google-Workspace.svg',        46, 41),
 ('Computer-Repairs-Icon.png',           'Computer-Repairs.svg',        46, 43),
 ('VA-Recruitment-Services-Icon.png',    'VA-Recruitment-Services.svg', 46, 46),
]
PATS = [(re.compile(r'<img src="((?:\.\./)*images/submenus/)' + re.escape(old) + r'"[^>]*>'), new, w, h)
        for old, new, w, h in MAP]

files = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('dump', 'images', 'videos', 'featured-images')]
    for f in fn:
        if f.endswith('.html'):
            files.append(os.path.join(dp, f))

changed = 0; total = 0; misses = []
for p in sorted(files):
    s = open(p, encoding='utf-8').read()
    o = s; n = 0
    for pat, new, w, h in PATS:
        rep = '<img src="\\g<1>%s" alt="" width="%d" height="%d" loading="lazy" decoding="async">' % (new, w, h)
        s, k = pat.subn(rep, s)
        n += k
    if s != o:
        open(p, 'w', encoding='utf-8', newline='').write(s)
        changed += 1; total += n
        if n != 8:
            misses.append((os.path.relpath(p, ROOT), n))
print('files changed:', changed, ' img tags replaced:', total)
if misses: print('PARTIAL:', misses[:20])
