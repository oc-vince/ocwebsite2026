# -*- coding: utf-8 -*-
import sys, os, json, re
sys.path.insert(0, os.path.expanduser('~/oc_build'))
from assemble import build
BUILD = os.path.expanduser('~/oc_build')

CHK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.6l4.4 4.4L19 7.4"/></svg>'

CASES = [
 dict(hero='BillW.webp', slug='billw', n='01', name='Bill W. Conscious Contact', tag='Documentary &amp; publishing',
   url='https://billwconsciouscontact.com/', domain='billwconsciouscontact.com',
   cats=['web','marketing','hosting'],
   blurb="A documentary film and a book, with one job between them: reach an audience and sell. We built the site around both of those tasks rather than one &mdash; a film to promote and a catalogue to sell &mdash; then ran the digital marketing that drives people to it, produced the creatives and banners the campaigns needed, and kept the site hosted and maintained so a launch week never turned into a technical one.",
   handle=["Web design and development tailored to a documentary film and selling books",
           "Digital marketing aimed at selling the movie and the books",
           "Creatives and banners for the campaigns",
           "Website maintenance and hosting"]),
 dict(hero='vbm-hero.webp', slug='velocity', n='02', name='Velocity Brand Management', tag='The full brief',
   url='https://www.vbmglobal.com/', domain='vbmglobal.com',
   cats=['it','web','marketing','hosting'],
   blurb="The widest brief we run, and the clearest example of what one partner actually means. Velocity's technology and marketing both sit with us: the IT their people use day to day, the website, its hosting and maintenance, the digital marketing, and the creative work that feeds all of it. One team, one invoice, and nobody in the middle translating between suppliers.",
   handle=["Managed IT support for the business",
           "Web development, website maintenance and hosting",
           "Digital marketing",
           "Creatives"]),
 dict(hero='benjaminlaw-hero.webp', slug='benjamin', n='03', name='Benjamin Lawyers', tag='Legal',
   url='https://www.benjaminlaw.com.au/', domain='benjaminlaw.com.au',
   cats=['it','hosting'],
   blurb="A law firm's systems have to be dependable and, ideally, invisible. We look after Benjamin Lawyers' managed IT support, host the website and maintain it &mdash; patched, backed up and monitored &mdash; so the practice spends its attention on client work rather than on technology.",
   handle=["Managed IT support for the firm", "Web hosting", "Website maintenance"]),
 dict(hero='SydneyRetreat-hero.webp', slug='sydney-retreat', n='04', name='The Sydney Retreat', tag='Not-for-profit',
   url='https://www.thesydneyretreat.org.au/', domain='thesydneyretreat.org.au',
   cats=['it','hosting'],
   blurb="A 12 step recovery program that people reach out to at genuinely difficult moments, which makes uptime more than a technical metric. We provide the managed IT support, the hosting and the ongoing maintenance behind it &mdash; and the same team looks after the systems, the hosting and the site itself.",
   handle=["Managed IT support for the organisation", "Web hosting", "Website maintenance"],
   ),
 dict(hero='allworkx.webp', slug='allworx', n='05', name='All Worx Electrical', tag='Trades &amp; contracting',
   url='https://www.allworx.au/', domain='allworx.au',
   cats=['it','hosting'],
   blurb="An electrical contractor with crews on the road and an office that cannot afford to stop. We handle All Worx Electrical Pty Ltd's managed IT support, host the website and keep it maintained, so a laptop failing on a Tuesday morning is our problem to solve rather than theirs.",
   handle=["Managed IT support for the company", "Web hosting", "Website maintenance"]),
]

WORK = [
 ('Bill W Conscious Contact',        'https://billwconsciouscontact.com/',           'BillW.webp',            'web branding'),
 ('Jake McKinley',                   'https://jakelaw.com.au/',                      'JakeMcKinley.webp',     'web'),
 ('Fireside Heating',                'https://www.firesideheating.com.au/',          'fireside.webp',         'web branding'),
 ('Velocity Brand Management',       'https://www.vbmglobal.com/',                   'VBM.webp',              'web branding'),
 ('Heat Cool Mist Co.',              'https://heatcoolmist.au/',                     'heatcoolmist.webp',     'web branding'),
 ('Sam Crawford Photography',        'https://samcrawford.au/',                      'SamCrawford.webp',      'web'),
 ('Australian Locating Services',    'https://www.locating.com.au/',                 'locatingau.webp',       'web'),
 ('Hortkraft Garden Maintenance',    'https://www.hortkraft.com/',                   'hortkraft.webp',        'web branding'),
 ('Craig &amp; Co.',                 'https://craigandco.com.au/',                   'craigandco.webp',       'web branding'),
 ('Get a Handyman',                  'https://getahandyman.au/',                     'handyman.webp',         'web branding'),
 ('Laser Therapy Sydney',            'https://www.lightbed.com.au/',                 'lightbed.webp',         'web branding'),
 ('St. Columbans Turramurra',        'https://stcolumbans.com.au/',                  'stcolumbans.webp',      'web'),
 ('The Rug &amp; Fabric Care Company','https://rugandfabriccare.com.au/',            'rugfabric.webp',        'web branding'),
 ('Chief Plumbing Services',         'https://chiefplumbing.com.au/',                'chiefplumbing.webp',    'web'),
 ('My Surf Photo',                   'https://www.mysurf.photo/',                    'mysurf.webp',           'web branding'),
 ('Pressure &amp; Steam',            'https://pressureandsteam.com.au/',             'pressuresteam.webp',    'web branding'),
 ('Maniscalco Stone',                'http://www.maniscalcostone.com/',              'maniscalco.webp',       'web'),
 ('Southern Highlands Yoga',         'https://mittagongyoga.com.au/',                'mittagongyoga.webp',    'web'),
 ('NRSC Services',                   'https://nrscservices.com.au/',                 'nrsc.webp',             'web branding'),
 ('Southern Cross Automotive',       'https://www.southerncrossautorepairs.com.au/', 'scar.webp',             'web'),
 ('LME Electrical',                  'https://www.lmeelectrical.com.au/',            'lme.webp',              'web'),
 ('Elle J Hair',                     'https://www.ellejhair.com.au/',                'ellej.webp',            'web branding'),
 ('Fresh Produce Group',             'https://fpg.com.au/',                          'fpg.webp',              'web branding'),
 ('David Jones The Electrician',     'https://djelectrician.com.au/',                'dje.webp',              'web branding'),
 ('Powe Partners',                   'https://www.powepartners.com.au/',             'powe.webp',             'web'),
 ('Smart Berries',                   'https://www.smartberries.com.au/',             'smartberries.webp',     'web branding'),
 ('V-Mark Survey',                   'https://vmarksurvey.com.au/',                  'vmark.webp',            'web'),
 ('Kai Kalda Interiors',             'https://www.kaikaldainteriors.com.au/',        'kaikalda.webp',         'web'),
 ('QVS Group',                       'https://qvsgroup.com.au/',                     'qvs.webp',              'web'),
 ('You&amp;Eye Optical',             'https://www.youandeye.com.au/',                'youandeye.webp',        'web branding'),
 ('Loving Sober',                    'https://lovingsober.com/',                     'lovingsober.webp',      'web'),
 ('Sinclair Wilde',                  'https://www.sinclairwilde.com.au/',            'sinclair.webp',         'web'),
 ("Sydney Men's Weekend",            'https://www.sydneymensweekend.com.au/',        'sydneymensweekend.webp','web'),
 ('Tin Horse Ranch',                 'https://www.tinhorseranch.com.au/',            'tinhorse.webp',         'web'),
 ('Betta Storage Containers',        'https://www.bettastorage.com.au/',             'bettastorage.webp',     'web'),
 ('Universal Tech Solutions',        'https://www.universaltech.net.au/',            'universaltech.webp',    'web'),
 ('SecureSoft',                      'https://securesoft.com.au/',                   'securesoft.webp',       'web'),
 ('Viska',                           'https://viska.au/',                            'viska.webp',            'web'),
 ('Mainsheet',                       'https://www.mainsheet.com.au/',                'mainsheet.webp',        'web'),
 ('Cosmic Sleep Clinic',             'https://cosmicsleepclinic.com.au/',            'cosmicsleep.webp',      'web branding'),
 ('CS1 Group',                       'https://cs1group.com.au/',                     'cs1group.webp',         'web'),
 ("Sydney Men's Camp",               'https://sydneymenscamp.au/',                   'sydneymenscamp.webp',   'web'),
 ('Coffs Containers',                'https://www.coffscontainers.com.au/',          'coffs.webp',            'web'),
 ('Sydney Legal Advisers',           'https://sydlegal.com.au/',                     'sydneylegal.webp',      'web'),
 ('NSCSO',                           'https://nscso.org.au/',                        'nscso.webp',            'web'),
 ('Southern Cross Funerals',         'https://southerncrossfunerals.com/',           'southerncross.webp',    'web'),
 ('Hunter Containers',               'https://huntercontainers.com.au/',             'huntercontainers.webp', 'web'),
 ('FHMS',                            'https://www.handymannorthernbeaches.com.au/',  'fhms.webp',             'web'),
 ('Mega Trucks &mdash; Aftermarket Parts Brochure', 'archives/prints/MegaTrucksAU-brochure.pdf',
                                                    'prints/MegaTrucksAU-brochure.webp',           'prints'),
 ('Pressure &amp; Steam &mdash; Medical and Forensic Cleaning Services Brochure', 'archives/prints/PressureAndSteam-COVIDBrochure.pdf',
                                                    'prints/PressureAndSteam-COVIDBrochure.webp',  'prints'), ('Online Consulting 2017 Reel',      'https://youtu.be/WOxZwi5uFis?si=e57VDMBwSrSiVq7C', 'video/oc-reel-2017.webp', 'videos'),
 ('Vivid Sydney 2013 &mdash; Time Lapse','https://vimeo.com/69538833',                'video/vividtime.webp',    'videos'),
 ('Lip Nourish',                       'https://vimeo.com/71389799',                  'video/lipnourish.webp',   'videos'),
 ("Joe's Garage Gym",                  'https://vimeo.com/68194191',                  'video/joesgarage.webp',   'videos'),
 ('Vivid Sydney 2012 &mdash; Time Lapse','https://vimeo.com/68843355',                 'video/vivid-2012.webp',   'videos'),
 ('Everyone Loves To Press Play',      'https://vimeo.com/64472332',                  'video/pressplay.webp',    'videos'),
]

def frame(c, lead=False):
    return """      <div class="cs__media" data-reveal>
        <span class="cs__idx" aria-hidden="true">%(n)s</span>
        <a class="cs__shot" href="%(url)s" target="_blank" rel="noopener" aria-label="Visit %(name)s (opens in a new tab)">
          <img src="images/portfolio/%(hero)s" alt="The %(name)s website" decoding="async" loading="lazy">
          <span class="cs__go" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M7 17L17 7M9.4 7H17v7.6"/></svg></span>
        </a>
      </div>
"""  % c

def body(c):
    lis = '\n'.join('            <li>%s<span>%s</span></li>' % (CHK, h) for h in c['handle'])
    return """      <div class="cs__body">
        <span class="cs__tag" data-reveal>%s</span>
        <h3 class="reveal-lines">%s</h3>
        <p class="cs__blurb" data-reveal>%s</p>
        <div class="cs__handle" data-reveal>
          <b>What we handle</b>
          <ul>
%s
          </ul>
        </div>
        <a class="cs__visit" href="%s" target="_blank" rel="noopener" data-magnetic><span>Visit %s</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M9.4 7H17v7.6"/></svg></a>
        %s
      </div>
""" % (c['tag'], c['name'], c['blurb'], lis, c['url'], c['domain'], c.get('extra',''))

rows = []
for i, c in enumerate(CASES):
    rows.append('        <article class="csx__slide" id="case-%s" role="group" aria-roledescription="slide" aria-label="%d of %d: %s">\n          <div class="csx__inner">\n%s%s          </div>\n        </article>\n'
                % (c['slug'], i+1, len(CASES), c['name'], frame(c), body(c)))

grid = []
PDF_ICON = ('<svg viewBox="0 0 24 24"><path d="M13.4 3.2H7a2 2 0 0 0-2 2v13.6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8.8z"/>'
            '<path d="M13.4 3.2v5.6H19"/></svg>')
LINK_ICON = '<svg viewBox="0 0 24 24"><path d="M7 17L17 7M9.4 7H17v7.6"/></svg>'

def vid_id(url):
    """youtube -> yt:ID[?si=...], vimeo -> vm:ID[?h=...]"""
    m = re.search(r'[?&]v=([A-Za-z0-9_-]+)', url) or re.search(r'youtu\.be/([A-Za-z0-9_-]+)', url)
    if m:
        si = re.search(r'[?&]si=([A-Za-z0-9_-]+)', url)
        return 'yt:' + m.group(1) + ('?si=' + si.group(1) if si else '')
    m = re.search(r'vimeo\.com/(\d+)(?:/([A-Za-z0-9]+))?', url)
    if m:
        return 'vm:' + m.group(1) + ('?h=' + m.group(2) if m.group(2) else '')
    return ''

for name, url, thumb, cat in WORK:
    src  = thumb if thumb.startswith('http') else 'images/portfolio/' + thumb
    kind = 'videos' if cat == 'videos' else ('pdf' if url.lower().endswith('.pdf') else 'site')
    plain = name.replace('&amp;', 'and').replace('&mdash;', '-')
    if kind == 'videos':
        alt  = '%s - video still' % plain
        icon = ('<svg viewBox="0 0 24 24" class="pf-tri" aria-hidden="true">'
                '<path d="M9 7.6l8 4.4-8 4.4z" fill="currentColor" stroke="none"/></svg>')
        attrs = ' href="%s" data-video="%s" data-title="%s"' % (url, vid_id(url), name)
    elif kind == 'pdf':
        alt  = '%s brochure, opens as a PDF' % plain
        icon = PDF_ICON
        attrs = ' href="%s" target="_blank" rel="noopener" type="application/pdf"' % url
    else:
        alt  = 'The %s website' % plain
        icon = LINK_ICON
        attrs = ' href="%s" target="_blank" rel="noopener"' % url
    grid.append("""      <a class="pf-item pf-item--%s"%s data-cat="%s" data-pf>
        <span class="pf-thumb"><img src="%s" alt="%s" loading="lazy" decoding="async"></span>
        <span class="pf-go" aria-hidden="true">%s</span>
        <span class="pf-meta"><b>%s</b></span>
      </a>\n""" % (kind, attrs, cat, src, alt, icon, name))

MAIN = """<main id="main">

<!-- ============ HERO ============ -->
<section class="hero hero--page hero--book hero--work">
  <div class="container hero__inner">
    <nav class="crumbs" aria-label="Breadcrumb" data-reveal>
      <a href="index.html">Home</a><i>&rsaquo;</i><span>Our Work</span>
    </nav>
    <p class="hero__eyebrow" data-reveal><span class="eyebrow-seg">Case studies</span><span class="eyebrow-sep"> &middot; </span><span class="eyebrow-seg">IT, web &amp; marketing</span></p>
    <h1 class="reveal-lines" id="heroTitle">Our <span class="accent">Work</span></h1>
    <p class="hero__sub" data-reveal>Check out our work &mdash; the absolute best. Some clients come to us for a website, some for their IT, and some hand us the lot. Below are five we look after end to end, and the wider list of businesses we have built for.</p>
    <div class="hero__cta" data-reveal>
      <a class="btn btn--light" href="book.html" data-magnetic><span>Book a Free IT Review</span><span class="arrow">&rarr;</span></a>
      <a class="btn btn--ghost" href="#case-studies" data-magnetic><span>See the case studies</span></a>
      <a class="btn btn--ghost" href="#clients" data-magnetic><span>View our works</span></a>
    </div>
  </div>
</section>

<!-- ============ FEATURED CASE STUDIES ============ -->
<section class="op-sec" id="case-studies">
  <div class="container">
    <div class="op-head" data-reveal>
      <p class="section__kicker">Featured case studies</p>
      <h2 class="reveal-lines">Real Challenges. <br>Smarter Solutions. <br>Better Results.</h2>
      <p>From managed IT to websites and digital marketing, explore how we help our clients turn ideas and challenges into practical, high-performing solutions.</p>
    </div>
  </div>

  <div class="csx" id="csx">
    <div class="csx__viewport" id="csxViewport">
      <div class="csx__track" id="csxTrack">
%s      </div>
    </div>
    <div class="csx-bar">
      <div class="csx-arrows">
        <button class="csx-arrow" type="button" id="csxPrev" aria-label="Previous case study"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
        <button class="csx-arrow" type="button" id="csxNext" aria-label="Next case study"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>
      <div class="csx-dots" id="csxDots" role="tablist" aria-label="Choose a case study"></div>
      <div class="csx-rail"><i id="csxRail"></i></div>
      <p class="csx-count"><b id="csxNow">1</b> / <span id="csxTotal">5</span></p>
    </div>
  </div>
</section>

<!-- ============ MORE CLIENTS ============ -->
<section class="op-sec op-sec--tint" id="clients">
  <div class="container">
    <div class="op-head" data-reveal>
      <p class="section__kicker">More of our work</p>
      <h2 class="reveal-lines">Who else we have built for.</h2>
      <p>Filter by the kind of work.</p>
    </div>

    <div class="pf-filters" id="pfFilters" role="group" aria-label="Filter work by service">
      <button class="pf-filter is-active" type="button" aria-current="true" data-filter="all">All</button>
      <button class="pf-filter" type="button" data-filter="web">Web Development</button>
      <button class="pf-filter" type="button" data-filter="branding">Branding</button>
      <button class="pf-filter" type="button" data-filter="prints">Prints</button>
      <button class="pf-filter" type="button" data-filter="videos">Videos</button>
    </div>

    <div class="pf-grid" id="pfGrid">
%s    </div>
    <p class="pf-empty" id="pfEmpty" hidden>Nothing in that category yet &mdash; try another.</p>
  </div>
</section>

<!-- ============ CTA ============ -->
<section class="cta">
  <video class="cta__video" src="video/lab.mp4" autoplay muted loop playsinline preload="auto" aria-hidden="true"></video>
  <div class="cta__inner">
    <h2 class="reveal-lines">Ready to get started? <br>Keen to find out more?</h2>
    <p data-reveal>We'd love to help your business. Call or message us now and one of our friendly team will be happy to chat through some options with you.</p>
    <div class="cta__actions" data-reveal>
      <a class="btn btn--light" href="book.html" data-magnetic><span>Book a Free IT Review</span><span class="arrow">&rarr;</span></a>
      <a class="btn btn--ghost" href="tel:+61284597882" data-magnetic><span>Or call us now &mdash; +61 2 8459 7882</span></a>
    </div>
  </div>
</section>

<!-- ============ VIDEO LIGHTBOX ============ -->
<div class="vlx" id="vlx" role="dialog" aria-modal="true" aria-label="Video player" hidden>
  <div class="vlx__scrim" data-vlx-close></div>
  <button class="vlx__close" type="button" data-vlx-close aria-label="Close video">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
  </button>
  <div class="vlx__stage">
    <div class="vlx__frame" id="vlxFrame"></div>
    <p class="vlx__caption" id="vlxCaption"></p>
  </div>
</div>

</main>
""" % (''.join(rows), ''.join(grid))

open(os.path.join(BUILD,'work_main.html'),'w',encoding='utf-8',newline='\n').write(MAIN)

BASE='https://onlineconsulting.com.au/'
ORG={"@type":"Organization","name":"Online Consulting","url":BASE,"telephone":"+61 2 8459 7882",
     "address":{"@type":"PostalAddress","addressLocality":"Allambie Heights","addressRegion":"NSW","addressCountry":"AU"}}
import re
def plain(x): return re.sub(r'&mdash;','-',re.sub(r'&amp;','&',x))
ld={"@context":"https://schema.org","@graph":[
 {"@type":"CollectionPage","name":"Our Work","url":BASE+"work.html",
  "description":"Case studies and client work from Online Consulting - managed IT support, web design and development, hosting and digital marketing for Australian businesses.",
  "publisher":ORG},
 {"@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Home","item":BASE},
  {"@type":"ListItem","position":2,"name":"Our Work","item":BASE+"work.html"}]},
 {"@type":"ItemList","name":"Featured case studies","itemListElement":[
  {"@type":"ListItem","position":i,"item":{"@type":"CreativeWork","name":plain(c['name']),"url":c['url'],
   "description":plain(c['blurb'])[:300],"creator":{"@type":"Organization","name":"Online Consulting"}}}
  for i,c in enumerate(CASES,1)]}]}

build('one-partner.html','work.html',
 'Our Work | Case Studies &amp; Client Projects | Online Consulting Sydney',
 'Case studies from Online Consulting &mdash; managed IT support, web design and development, hosting and digital marketing for Australian businesses including Velocity Brand Management and Benjamin Lawyers.',
 BASE+'work.html','Our Work | Online Consulting',
 'Five businesses we look after end to end, and the wider list of clients we have built for. IT, web and marketing from one Sydney team.',
 ld,'work_css.txt','work_main.html')
