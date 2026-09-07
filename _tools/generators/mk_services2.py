import sys, os
sys.path.insert(0, os.path.expanduser('~/oc_build'))
from assemble import build
BASE='https://onlineconsulting.com.au/'
ORG={"@type":"Organization","name":"Online Consulting","url":BASE,"telephone":"+61 2 8459 7882",
     "address":{"@type":"PostalAddress","addressLocality":"Allambie Heights","addressRegion":"NSW","addressCountry":"AU"}}
def ld(name, slug, desc, svctype, faqs, offers=None):
    url=BASE+'service/'+slug+'/'
    svc={"@type":"Service","name":name,"serviceType":svctype,"url":url,"description":desc,
         "provider":ORG,"areaServed":{"@type":"Place","name":"Sydney, Australia"}}
    if offers: svc["hasOfferCatalog"]={"@type":"OfferCatalog","name":name+" packages","itemListElement":offers}
    return {"@context":"https://schema.org","@graph":[svc,
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE},
        {"@type":"ListItem","position":2,"name":name,"item":url}]},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}]}

TPL='service/it-support/index.html'

build(TPL,'service/web-development/index.html',
 'Web Design &amp; Development Sydney | Website Developers | Online Consulting',
 'Trusted web designers and web developers for Australian businesses. Website design, e-commerce, product galleries, copywriting and SEO from Sydney&#39;s Northern Beaches.',
 BASE+'service/web-development/','Web Design &amp; Development Sydney | Online Consulting',
 'Your website may be the first experience customers have with your business. We handle domain, design, build, content, SEO and the marketing that follows.',
 ld('Web Design & Development','web-development',
    'Website design and development services for Australian businesses - domain registration, responsive design, e-commerce, product galleries, copywriting, SEO and digital marketing.',
    'Web Design and Development',[
  ("What's actually included in a website build?","We handle the process from start to finish: finding and buying the right domain name, designing a great looking, fast loading website, including informative and engaging content, optimising your website for search engines, and expanding your reach with Google Ads and digital marketing."),
  ("Can you build an online shop or a product gallery?","Yes. We'll customise the site to your exact needs, helping you set up e-commerce facilities, product galleries and functionality for large quantities of data if required."),
  ("Do you only work with small businesses?","No. Our web developers are experts in all aspects of web design for small businesses as well as for larger organisations, and we work with customers around Australia and beyond."),
  ("Can you help with a logo as well?","Our graphic designer can even help with business logo design if you need it."),
  ("What happens after the site goes live?","We'll monitor the performance of your site to make sure it grows with you and achieves the best possible results, helping you rank well for important keywords and keep you there to maximise conversions."),
 ]),'svc2_css.txt','wd_main.html')

OFFERS=[
 {"@type":"Offer","name":"Premium Managed Virtual Private Server + WordPress Security Maintenance","price":"264","priceCurrency":"AUD",
  "description":"Dedicated virtual machine (1 CPU, 2GB RAM, 20GB SSD), CDN with Web Application Firewall, SSL, weekly VM snapshots and daily backups, WordPress updates, domain and DNS management, and up to 2 hours of alterations per month. Excludes GST."},
 {"@type":"Offer","name":"Premium Virtual Private Server Package","price":"99","priceCurrency":"AUD",
  "description":"Dedicated virtual machine (1 CPU, 2GB RAM, 20GB SSD), CDN with Web Application Firewall, SSL, weekly VM snapshots and daily backups, monitoring, 500GB traffic per month, domain and DNS management. Excludes GST."},
 {"@type":"Offer","name":"Manage your Own Hosting","price":"33","priceCurrency":"AUD",
  "description":"Up to 2GB file space, 30GB/month transfer, C-Panel access, hosted in a premium data centre in Ultimo Sydney, with daily, weekly and monthly backups to an alternate location. Excludes GST."}]

build(TPL,'service/web-hosting/index.html',
 'Web Hosting &amp; Domains Sydney | Managed Hosting &amp; Domain Names | Online Consulting',
 'Sydney web hosting from $33/month +GST &mdash; managed VPS, WordPress security maintenance, SSL, daily backups and domain name management from a Northern Beaches team.',
 BASE+'service/web-hosting/','Web Hosting &amp; Domains Sydney | Online Consulting',
 'Trusted, affordable Australian web hosting packages &mdash; dedicated virtual machines, SSL, daily backups and domain management, hosted in Sydney.',
 ld('Web Hosting & Domains','web-hosting',
    'Australian web hosting packages - managed and self-managed VPS hosting, WordPress security maintenance, SSL, daily backups, DNS and domain name management.',
    'Web Hosting',[
  ("What's the difference between the three hosting packages?","The two Premium packages put your site on a dedicated virtual machine, so all the resources on that server are dedicated to your website. The $264 plan adds WordPress security maintenance and up to 2 hours of alterations a month. Manage your Own Hosting at $33 is shared hosting with C-Panel access in a premium data centre in Ultimo, Sydney."),
  ("Is my domain renewal included in the price?","Domain name management is included on both Premium packages so your domain renewal never lapses, but the actual domain renewal price is not included in the monthly fee."),
  ("Where is my website actually hosted?","In Australia. Self-managed hosting sits in a premium data centre in Ultimo, Sydney, with daily, weekly and monthly backups performed to an alternate location to the server."),
  ("Do I get an SSL certificate?","Yes on both Premium packages - an SSL certificate and full HTTPS for the whole site, along with a CDN and Web Application Firewall to help mitigate DDOs and other such attacks."),
  ("Can you move my site from another host?","Yes. Whether you're launching a new website or looking to switch to a reliable web hosting provider, we're here to help, including handling the domain transfer from your current registrar."),
 ], OFFERS),'svc2_css.txt','wh_main.html')

build(TPL,'service/video/index.html',
 'Videography Sydney | Promotional &amp; Event Video Production | Online Consulting',
 'Sydney video production services &mdash; promotional videos, corporate and event video production, instructional videos and website video, shot and edited in our own studio.',
 BASE+'service/video/','Videography Sydney | Online Consulting',
 'Our Sydney video production services are an incredible way to capture attention and tell an immersive story. Nothing outsourced &mdash; all editing in our own studio.',
 ld('Videography','video',
    'Sydney video production services - promotional videos for products, corporate event video production, website video, instructional videos, event coverage and aerial drone video.',
    'Video Production',[
  ("What kinds of video do you produce?","Promotional videos for products, corporate event video production, website video production and more. We've helped businesses create memorable advertising, informative instructional videos and eye-catching event coverage."),
  ("I'm not comfortable on camera. Is that a problem?","Not at all. We don't try to transform people into actors. The best results come when people relax, be themselves and tell their story in a natural way."),
  ("Do I get different cuts for different platforms?","Yes. Once we're done filming we'll edit your video for use across various platforms to maximise reach and interest - for example cutting a five minute promotional video into a 30 second YouTube ad."),
  ("Is the editing done in-house?","Yes. Nothing about our video production service is outsourced. All of our post production and editing work happens in our studio."),
  ("How does a project start?","Talk to us about your needs and we'll guide you through the process, from an initial plan right the way through to the final content."),
 ]),'svc2_css.txt','vd_main.html')

build(TPL,'service/photography/index.html',
 'Photography Sydney | Event &amp; Commercial Photographers | Online Consulting',
 'Event and commercial photography tailored to your vision &mdash; corporate profiles, product shoots, aerial drone work, conferences, weddings and celebrations, from a Northern Beaches studio.',
 BASE+'service/photography/','Photography Sydney | Online Consulting',
 'Images say what words can&#39;t. A full suite of creative services from concept planning to post production, all handled in our own studio.',
 ld('Photography','photography',
    'Event and commercial photography services - corporate video and profiles, product shoots, aerial drone video, conferences and events, weddings, TVCs and portfolios.',
    'Photography',[
  ("What kinds of photography do you do?","A full range: corporate video and profiles; product videos and shoots including aerial video with drones; conferences and events; online video; scripting; TVCs; portfolios and video productions. And for weddings, events and celebrations we create memories you'll keep for generations."),
  ("Do you shoot weddings as well as commercial work?","Yes. For weddings, events and celebrations we create memories that you'll keep for generations, and our still and moving images are indispensable branding, promotional and marketing tools for your business."),
  ("Is any of the editing sent offshore?","No. Nothing about our Video Production Service is outsourced. All of our post production and editing work happens in our studio."),
  ("Can I use one shoot across several platforms?","Yes. A five minute promotional video can be edited into a 30 second YouTube promotion, and the same video can be adapted to other digital platforms."),
  ("How much planning goes in before the day?","A lot. Jarrad, our Production Manager, spends hours studying his brief and preparing the best angles and locations. He has contingencies for every conceivable event."),
 ]),'svc2_css.txt','ph_main.html')
