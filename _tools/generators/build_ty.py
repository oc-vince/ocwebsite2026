# -*- coding: utf-8 -*-
import os, re
SITE=os.path.expanduser('~/mnt/public'); BUILD=os.path.expanduser('~/ocblog')
def rd(p): return open(p,encoding='utf-8').read()

TPL=rd(os.path.join(SITE,'one-partner.html'))
TPL=re.sub(r'(href|src)="(?!https?:|//|/|#|mailto:|tel:|data:|\.\./)([^"]+)"', r'\1="../\2"', TPL)
TPL=TPL.replace('href="blog.html"','href="../blog.html"').replace('href="/blog/"','href="../blog.html"')
CSS=rd(os.path.join(BUILD,'ty_css.txt'))
MAIN=rd(os.path.join(BUILD,'ty_main.txt'))
NEXT=rd(os.path.join(BUILD,'ty_next.txt'))

def step(n,t,p):
    return ('      <div class="ty-step" data-reveal>\n'
            '        <em>%s</em>\n        <b>%s</b>\n        <p>%s</p>\n'
            '        <span class="ty-step__bar" aria-hidden="true"></span>\n      </div>' % (n,t,p))

PAGES = {
 'book/thank-you.html': dict(
   title='Thanks &mdash; your booking is in | Online Consulting',
   desc='Your consultation request has reached the Online Consulting team. We confirm every booking within two business hours.',
   canon='https://onlineconsulting.com.au/book/thank-you/',
   eyebrow='Booking received',
   h1='That&rsquo;s <span class="accent">booked in.</span> Thank you.',
   sub='Your request has landed with the right team &mdash; not a shared inbox. Someone who actually does the work will pick it up and confirm your time.',
   nexth2=None,
   nextsub=None,
   callp='If it can&rsquo;t wait for a confirmation email &mdash; an outage, a deadline, a site that&rsquo;s down &mdash; call the office and a person will answer.',
   steps=None),
 'contact/thank-you.html': dict(
   title='Thanks &mdash; your message is on its way | Online Consulting',
   desc='Your message has reached the Online Consulting team in Sydney. We reply to every enquiry within two business hours.',
   canon='https://onlineconsulting.com.au/contact/thank-you/',
   eyebrow='Message sent',
   h1='Got it. Your message is <span class="accent">on its way.</span>',
   sub='It&rsquo;s gone to our Sydney office, not an overseas queue.<br>One of the team will read it and come back to you personally.',
   nexth2='What happens between now and our reply.',
   nextsub='No auto-responder loop, no ticket number to memorise. Here is the honest version.',
   callp='If it&rsquo;s urgent &mdash; something&rsquo;s down, or you need an answer today &mdash; don&rsquo;t wait on email. Call the office and a person will answer.',
   steps=[('01','Our support agent will review','Your message goes to the team, not a bot. If it belongs with another part of the business we pass it across ourselves.'),
          ('02','We reply within 2 hours','During business hours you&rsquo;ll hear back inside two hours. Outside them, first thing the next working morning.'),
          ('03','You talk to the right person','Whoever replies is the person who can actually help &mdash; not a coordinator reading from a script.')]),
}

for path, d in PAGES.items():
    html = TPL
    html = re.sub(r'<title>.*?</title>', lambda _: '<title>'+d['title']+'</title>', html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content=".*?">',
                  lambda _: '<meta name="description" content="'+d['desc']+'">', html, count=1, flags=re.S)
    html = re.sub(r'<link rel="canonical" href=".*?">',
                  lambda _: '<link rel="canonical" href="'+d['canon']+'">', html, count=1, flags=re.S)
    html = re.sub(r'<meta property="og:title" content=".*?">',
                  lambda _: '<meta property="og:title" content="'+d['title']+'">', html, count=1, flags=re.S)
    html = re.sub(r'<meta property="og:description" content=".*?">',
                  lambda _: '<meta property="og:description" content="'+d['desc']+'">', html, count=1, flags=re.S)
    # keep these out of the index
    html = html.replace('<link rel="canonical"', '<meta name="robots" content="noindex, follow">\n<link rel="canonical"', 1)
    html = re.sub(r'<script type="application/ld\+json">.*?</script>',
                  '<script type="application/ld+json">\n{ "@context": "https://schema.org", "@type": "WebPage", "name": "Thank you", "isPartOf": { "@type": "WebSite", "name": "Online Consulting", "url": "https://onlineconsulting.com.au/" } }\n</script>',
                  html, count=1, flags=re.S)
    i=html.index('</style>'); html=html[:i]+CSS+html[i:]
    main = (MAIN.replace('__EYEBROW__', d['eyebrow']).replace('__H1__', d['h1']).replace('__SUB__', d['sub'])
                .replace('__CALLP__', d['callp']))
    if d.get('steps'):
        nxt = (NEXT.replace('__NEXTH2__', d['nexth2']).replace('__NEXTSUB__', d['nextsub'])
                   .replace('__STEPS__', '\n'.join(step(*x) for x in d['steps'])))
    else:
        nxt = ''
    main = main.replace('__NEXTSECTION__', nxt)
    a=html.index('<main id="main">'); b=html.index('</main>')+len('</main>')
    html=html[:a]+main.strip()+html[b:]
    out=os.path.join(SITE, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out,'w',encoding='utf-8',newline='\n').write(html)
    print('wrote', path, len(html), 'bytes')
