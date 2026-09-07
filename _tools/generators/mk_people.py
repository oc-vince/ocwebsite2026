# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.expanduser('~/oc_build'))
from assemble import build
from team_data import TEAM

BUILD = os.path.expanduser('~/oc_build')

cards = []
for i, t in enumerate(TEAM, 1):
    n = '%02d' % i
    pid = 'bio-' + t['slug']
    bio = '\n'.join('          <p>%s</p>' % p for p in t['bio'])
    cards.append("""      <button class="tm-card" type="button" id="card-{slug}" aria-expanded="false" aria-controls="{pid}" data-team>
        <span class="tm-photo" data-photo>
          <span class="tm-idx">{n}</span>
          <img src="images/team/{slug}.jpg" alt="{name}, {role} at Online Consulting" loading="lazy" onerror="this.parentNode.classList.add('is-mono')">
          <span class="tm-mono" aria-hidden="true">{ini}</span>
        </span>
        <span class="tm-body">
          <span class="tm-name">{name}</span>
          <span class="tm-role">{role}</span>
          <span class="tm-rule" aria-hidden="true"></span>
          <span class="tm-more">Read {first}'s story <span class="tm-plus" aria-hidden="true"></span></span>
        </span>
      </button>
      <div class="tm-panel" id="{pid}" role="region" aria-label="About {name}" data-owner="card-{slug}">
        <div class="tm-panel__clip">
        <div class="tm-panel__box">
          <div class="tm-panel__aside">
            <div class="tm-shot" data-photo>
              <img src="images/team/{slug}.jpg" alt="" loading="lazy" onerror="this.parentNode.classList.add('is-mono')">
              <span class="tm-mono" aria-hidden="true">{ini}</span>
            </div>
            <div class="tm-motto"><b>Motto</b><q>{motto}</q></div>
          </div>
          <div class="tm-panel__main">
            <div class="tm-panel__head">
              <h3>{name}</h3><span>{role}</span>
            </div>
            <div class="tm-bio">
{bio}
            </div>
            <button class="tm-close" type="button" data-close><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>Close</button>
          </div>
        </div>
        </div>
      </div>
""".format(pid=pid, n=n, slug=t['slug'], name=t['name'], role=t['role'], ini=t['ini'],
           first=t['name'].split()[0], motto=t['motto'], bio=bio))

MAIN = """<main id="main">

<!-- ============ HERO ============ -->
<section class="hero hero--page hero--book hero--team">
  <div class="container hero__inner">
    <nav class="crumbs" aria-label="Breadcrumb" data-reveal>
      <a href="index.html">Home</a><i>&rsaquo;</i><span>Our Team</span>
    </nav>
    <p class="hero__eyebrow" data-reveal><span class="eyebrow-seg">The people behind the work</span><span class="eyebrow-sep"> &middot; </span><span class="eyebrow-seg">Australia, Vietnam &amp; the Philippines</span></p>
    <h1 class="reveal-lines" id="heroTitle">Our <span class="accent">Team</span></h1>
    <p class="hero__sub" data-reveal>We understand that a website should not only look great, it needs to get results. The Online Consulting team is the ideal mix of creativity, strategy, technical know-how, and reliability.</p>
    <div class="hero__cta" data-reveal>
      <a class="btn btn--light" href="book.html" data-magnetic><span>Book a Free IT Review</span><span class="arrow">&rarr;</span></a>
      <a class="btn btn--ghost" href="#the-team" data-magnetic><span>Meet the team</span></a>
    </div>
  </div>
</section>

<!-- ============ INTRO ============ -->
<section class="op-sec">
  <div class="container">
    <div class="tm-intro">
      <div>
        <p class="section__kicker" data-reveal>How we work together</p>
        <h2 class="reveal-lines">We work together closely to deliver your project <em>on time and on budget.</em></h2>
      </div>
      <div class="tm-intro__body">
        <p class="lead" data-reveal>We understand that a website should not only look great, it needs to get results. The Online Consulting team is the ideal mix of creativity, strategy, technical know-how, and reliability.</p>
        <p data-reveal>Each client has a designated Project Manager to liaise between you and the team. Lots of things need to come together when we build a website and we have fantastic Project Managers who know the process inside out.</p>
        <p data-reveal>We meet with you regularly to make sure the process is in line with your original concept. If you've had a rethink and you need to make some changes, that's not uncommon with websites and web development, so we adapt accordingly. If we need to tweak we tweak &mdash; if not, it's full steam ahead to testing and then we go live.</p>
        <div class="tm-pm" data-reveal>
          <i><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3.2"/><path d="M3.4 19.4a5.8 5.8 0 0 1 11.2 0"/><path d="M16.4 5.4a3 3 0 0 1 0 5.5M18.2 19.4a5.6 5.6 0 0 0-2.2-4.2"/></svg></i>
          <span>One designated Project Manager per client &mdash; your single point of contact into the whole team.</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============ THE TEAM ============ -->
<section class="op-sec op-sec--tint" id="the-team">
  <div class="container">
    <div class="op-head" data-reveal>
      <p class="section__kicker">Meet the team</p>
      <h2 class="reveal-lines">Nine people. <br>One very close team.</h2>
      <p>Click anyone to read their story &mdash; what they do here, and what they get up to when they're not doing it.</p>
    </div>
    <div class="tm-grid" id="teamGrid">
%s    </div>
  </div>
</section>

<!-- ============ REACH ============ -->
<section class="op-sec op-sec--dark">
  <div class="container">
    <div class="op-head" data-reveal>
      <p class="section__kicker">One team, three countries</p>
      <h2 class="reveal-lines">From Australia to Vietnam <br>and on to the Philippines.</h2>
      <p>Sam has built an international team that is able to deliver the &lsquo;big picture dream&rsquo; he sees for his clients. The fact that the team stretches this far is testament to his ability to share that vision with others.</p>
    </div>
    <div class="tm-reach">
      <article class="tm-loc" data-reveal><i>AU</i><b>Australia</b><span>Sydney &mdash; Northern Beaches to the CBD. Creative direction, project management, video and photography, and the people you'll meet face to face.</span></article>
      <article class="tm-loc" data-reveal><i>VN</i><b>Vietnam</b><span>Web development. Experienced developers with the patience to see the tiny details that create the perfect result for our clients.</span></article>
      <article class="tm-loc" data-reveal><i>PH</i><b>Philippines</b><span>Manila &mdash; content, client liaison, quality control, digital marketing and the IT Help Desk that keeps your support turning around quickly.</span></article>
    </div>
  </div>
</section>

<!-- ============ CTA ============ -->
<section class="cta">
  <video class="cta__video" src="video/lab.mp4" autoplay muted loop playsinline preload="auto" aria-hidden="true"></video>
  <div class="cta__inner">
    <h2 class="reveal-lines">Like to put this team <br>to work on your project?</h2>
    <p data-reveal>We'd love to help your business. Call or message us now and one of our friendly team will be happy to chat through some options with you.</p>
    <div class="cta__actions" data-reveal>
      <a class="btn btn--light" href="book.html" data-magnetic><span>Book a Free IT Review</span><span class="arrow">&rarr;</span></a>
      <a class="btn btn--ghost" href="tel:+61284597882" data-magnetic><span>Or call us now &mdash; +61 2 8459 7882</span></a>
    </div>
  </div>
</section>

</main>
""" % ''.join(cards)

open(os.path.join(BUILD,'people_main.html'),'w',encoding='utf-8',newline='\n').write(MAIN)

ORG = {"@type":"Organization","name":"Online Consulting","url":"https://onlineconsulting.com.au/","telephone":"+61 2 8459 7882",
       "address":{"@type":"PostalAddress","addressLocality":"Allambie Heights","addressRegion":"NSW","addressCountry":"AU"}}
import re
def plain(x): return re.sub(r'&[a-z]+;', lambda m: {'&mdash;':'-','&lsquo;':"'",'&rsquo;':"'",'&hellip;':'...','&amp;':'&'}.get(m.group(0), ''), x)
ld = {"@context":"https://schema.org","@graph":[
  {"@type":"AboutPage","name":"Our Team","url":"https://onlineconsulting.com.au/people.html",
   "description":"Meet the Online Consulting team - the mix of creativity, strategy, technical know-how and reliability behind our IT, web and digital marketing work.",
   "publisher":ORG},
  {"@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://onlineconsulting.com.au/"},
    {"@type":"ListItem","position":2,"name":"Our Team","item":"https://onlineconsulting.com.au/people.html"}]},
  {"@type":"ItemList","name":"Online Consulting team","itemListElement":[
    {"@type":"ListItem","position":i,"item":{"@type":"Person","name":t['name'],"jobTitle":plain(t['role']),
     "worksFor":{"@type":"Organization","name":"Online Consulting"},
     "description":plain(t['bio'][0])}} for i,t in enumerate(TEAM,1)]}
]}

build('one-partner.html','people.html',
 'Our Team | The People Behind Online Consulting | Sydney IT &amp; Digital Agency',
 'Meet the Online Consulting team &mdash; the mix of creativity, strategy, technical know-how and reliability behind our IT support, web development and digital marketing work.',
 'https://onlineconsulting.com.au/people.html',
 'Our Team | Online Consulting',
 'Nine people across Australia, Vietnam and the Philippines. Meet the team behind Online Consulting&#39;s IT, web and marketing work.',
 ld, 'team_css.txt','people_main.html')
