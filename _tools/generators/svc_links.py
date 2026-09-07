# -*- coding: utf-8 -*-
import os, re
P = os.path.expanduser('~/mnt/Version 2/index.html')
s = open(P, encoding='utf-8').read()

CSS = '''
/* ---- Service-card sub-links: mega-menu SVG icon + label (replaces the old chips) ---- */
.svc-links{display:grid;grid-auto-flow:column;grid-template-columns:repeat(2,minmax(0,1fr));
  gap:2px clamp(12px,1.8vw,26px);margin-top:4px;}
.service-card--featured .svc-links{grid-template-rows:repeat(4,auto);}
.services-row .svc-links{grid-template-rows:repeat(2,auto);}
.svc-link{position:relative;isolation:isolate;display:grid;grid-template-columns:30px minmax(0,1fr);
  align-items:center;gap:12px;padding:9px 12px;margin-left:-12px;border-radius:12px;
  transition:transform .38s var(--ease);}
/* tint sweeps in from the left, behind the row */
.svc-link::before{content:"";position:absolute;inset:0;z-index:-1;border-radius:inherit;
  background:linear-gradient(90deg,rgba(20,135,216,.13),rgba(20,135,216,0));
  opacity:0;transform:translateX(-10px);
  transition:opacity .38s var(--ease),transform .38s var(--ease);}
.svc-link:hover,.svc-link:focus-visible{transform:translateX(4px);}
.svc-link:hover::before,.svc-link:focus-visible::before{opacity:1;transform:none;}
.svc-link__ico{position:relative;width:30px;height:30px;display:grid;place-items:center;flex:0 0 auto;}
/* halo blooms out behind the icon */
.svc-link__ico::before{content:"";position:absolute;inset:-8px;border-radius:50%;
  background:radial-gradient(circle,rgba(20,135,216,.26),rgba(20,135,216,0) 70%);
  opacity:0;transform:scale(.55);
  transition:opacity .42s var(--ease),transform .42s var(--ease);}
.svc-link:hover .svc-link__ico::before,.svc-link:focus-visible .svc-link__ico::before{opacity:1;transform:none;}
.svc-link__ico img{position:relative;max-width:100%;max-height:100%;width:auto;height:auto;display:block;
  transition:transform .42s var(--ease);}
.svc-link:hover .svc-link__ico img,.svc-link:focus-visible .svc-link__ico img{transform:translateY(-2px) scale(1.12);}
.svc-link__label{position:relative;min-width:0;font-size:15px;font-weight:500;line-height:1.35;
  color:var(--grey);transition:color .3s var(--ease);}
.svc-link:hover .svc-link__label,.svc-link:focus-visible .svc-link__label{color:var(--blue);}
/* gradient underline draws out from the left */
.svc-link__label::after{content:"";position:absolute;left:0;right:0;bottom:-3px;height:1.5px;border-radius:2px;
  background:linear-gradient(90deg,var(--blue),rgba(20,135,216,0));
  transform:scaleX(0);transform-origin:left;transition:transform .45s var(--ease);}
.svc-link:hover .svc-link__label::after,.svc-link:focus-visible .svc-link__label::after{transform:scaleX(1);}
.svc-link:focus-visible{outline:2px solid var(--blue);outline-offset:2px;}
@media (max-width:640px){
  .svc-links,.service-card--featured .svc-links,.services-row .svc-links{
    grid-auto-flow:row;grid-template-columns:minmax(0,1fr);grid-template-rows:auto;}
}
@media (prefers-reduced-motion:reduce){
  .svc-link,.svc-link::before,.svc-link__ico::before,.svc-link__ico img,
  .svc-link__label,.svc-link__label::after{transition-duration:.01ms!important;}
  .svc-link:hover,.svc-link:focus-visible{transform:none;}
}
'''

ANCHOR = '.chip:hover{border-color:var(--blue);color:var(--blue);transform:translateY(-2px);}\n'
assert ANCHOR in s, 'chip anchor not found'
s = s.replace(ANCHOR, ANCHOR + CSS, 1)

def block(indent, items):
    out = [indent + '<div class="svc-links">']
    for href, svg, w, h, label in items:
        out.append(indent + '  <a class="svc-link" href="%s">' % href)
        out.append(indent + '    <span class="svc-link__ico"><img src="images/submenus/%s" alt="" width="%d" height="%d" loading="lazy" decoding="async"></span>' % (svg, w, h))
        out.append(indent + '    <span class="svc-link__label">%s</span>' % label)
        out.append(indent + '  </a>')
    out.append(indent + '</div>')
    return '\n'.join(out)

IT = [
 ('service/it-support/index.html','IT-Support-in-Sydney.svg',41,46,'IT Support in Sydney'),
 ('service/it-support/index.html#managed-cyber-security-support','Managed-Cyber-Security.svg',46,45,'Managed Cyber Security'),
 ('service/it-support/index.html#managed-network-packages','Managed-Network.svg',42,46,'Managed Network'),
 ('service/it-support/index.html#robust-cloud-backup','Robust-Cloud-Backup.svg',46,46,'Robust Cloud Backup'),
 ('service/it-support/index.html#ongoing-maintenance','Ongoing-Maintenance.svg',46,46,'Ongoing Maintenance'),
 ('service/google-workspace/index.html','Google-Workspace.svg',46,41,'Google Workspace'),
 ('service/computer-repairs/index.html','Computer-Repairs.svg',46,43,'Computer Repairs'),
 ('service/va-recruitment-services/index.html','VA-Recruitment-Services.svg',46,46,'VA Recruitment Services'),
]
DM = [
 ('service/seo-services/index.html','SEO-Services.svg',46,38,'SEO Services'),
 ('service/google-adwords/index.html','Google-Ads.svg',46,44,'Google Ads'),
 ('service/social-media-marketing/index.html','Social-Media-Marketing.svg',43,46,'Social Media Marketing'),
 ('service/copywriting/index.html','Content-Copywriting.svg',46,44,'Content &amp; Copywriting'),
]
WD = [
 ('service/web-development/index.html','Web-Design.svg',46,38,'Web Design &amp; Development'),
 ('service/web-hosting/index.html','Web-Hosting.svg',46,46,'Web Hosting &amp; Domains'),
 ('service/video/index.html','Videography.svg',39,46,'Videography'),
 ('service/photography/index.html','Photography.svg',46,35,'Photography'),
]

blocks = [IT, DM, WD]
pat = re.compile(r'([ \t]*)<div class="service-card__links">.*?</div>\n', re.S)
found = pat.findall(s)
assert len(found) == 3, 'expected 3 service-card__links blocks, found %d' % len(found)

it = iter(blocks)
def repl(m):
    return block(m.group(1), next(it)) + '\n'
s = pat.sub(repl, s, count=3)

open(P, 'w', encoding='utf-8', newline='').write(s)
print('ok  svc-link rows:', s.count('class="svc-link"'), ' chips left:', s.count('class="chip"'))
