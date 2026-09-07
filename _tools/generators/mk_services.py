import sys, os
sys.path.insert(0, os.path.expanduser('~/oc_build'))
from assemble import build
BASE='https://onlineconsulting.com.au/'
ORG = {"@type":"Organization","name":"Online Consulting","url":BASE,"telephone":"+61 2 8459 7882",
       "address":{"@type":"PostalAddress","addressLocality":"Allambie Heights","addressRegion":"NSW","addressCountry":"AU"}}

def ld(name, slug, desc, svctype, faqs):
    url = BASE + 'service/' + slug + '/'
    return {"@context":"https://schema.org","@graph":[
      {"@type":"Service","name":name,"serviceType":svctype,"url":url,"description":desc,
       "provider":ORG,"areaServed":{"@type":"Place","name":"Sydney, Australia"}},
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE},
        {"@type":"ListItem","position":2,"name":name,"item":url}]},
      {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    ]}

TPL='service/google-workspace/index.html'

# --- SEO ---
build(TPL,'service/seo-services/index.html',
 'SEO Services Sydney | Trusted SEO Specialists &amp; Consulting | Online Consulting',
 'Sydney SEO services from a local SEO specialist &mdash; in-depth audits, keyword research, on-page optimisation, link building, content and paid search, with regular reporting.',
 BASE+'service/seo-services/',
 'SEO Services Sydney | Online Consulting',
 'Work with trusted SEO specialists for long-term growth. Audits, keyword research, on-page SEO, link building and reporting from a Sydney team.',
 ld('SEO Services','seo-services',
    'Sydney SEO consulting services - audits, keyword research, on-page optimisation, link building, content creation and paid search, with regular performance reporting.',
    'Search Engine Optimisation',[
   ("What does an SEO audit actually look at?","An audit answers how search engine friendly your website is, with detailed information about keyword rankings, technical on page SEO and conversion rates, so we can see how well your site is performing and set objectives to improve it."),
   ("How do you decide which keywords to target?","Keyword research identifies words and phrases people are using to find products and services like yours on Google and other search engines. We'll identify and target those to get you ranking."),
   ("Do links to my site still matter?","Yes. High quality links to your website can improve your Google rankings. We'll help you understand why this matters and advise successful link building strategies that get you great results."),
   ("Should I be doing paid search as well as SEO?","For the best results you'll want to target paid search as well as organic search. Talk to us about pay per click and Google Ads and we'll find the keywords your audience is using, then manage your budget to get the best results."),
   ("How will I know whether it's working?","We track your site's performance and send you regular reports, giving us flexibility to move with the market and the way your audience is searching."),
 ]),'svc_css.txt','seo_main.html')

# --- SOCIAL ---
build(TPL,'service/social-media-marketing/index.html',
 'Social Media Marketing Sydney | Facebook &amp; Instagram Ads | Online Consulting',
 'Social media marketing services in Sydney &mdash; Facebook, Instagram and LinkedIn campaigns, Ads Manager setup, boosted posts, remarketing and conversion tracking.',
 BASE+'service/social-media-marketing/',
 'Social Media Marketing Sydney | Online Consulting',
 'Maximise your reach with strategic social media marketing. Tailored ad campaigns, boosted posts and tracking across Facebook, Instagram and LinkedIn.',
 ld('Social Media Marketing','social-media-marketing',
    'Social media marketing services in Sydney - tailored Facebook, Instagram and LinkedIn ad campaigns, boosted posts, remarketing and conversion tracking.',
    'Social Media Marketing',[
   ("What is social media marketing?","Social media marketing is a type of digital marketing used to promote your organisation's products and services online. It's achieved by creating and sharing content on social media platforms, including Facebook, LinkedIn and Instagram - organic posts for existing followers, or ads to reach new people."),
   ("Why do I need to boost posts?","One of the best reasons to boost posts is to get them in front of more eyes and overcome the decline in Facebook's organic reach. In short, your fans may not see posts or updates unless you boost them."),
   ("What do you set up when a campaign starts?","Facebook pixel in Google Tag Manager, general and billing information, geo-targeting for each ad, a remarketing campaign for site visitors saved in the pixel audience list, detailed targeting based on demographics, interests and behaviours, and conversion tracking."),
   ("Is this a one-off project or ongoing?","Social media marketing campaigns are an ongoing process. We track the performance of all posts, which allows us to respond to what works and move on fast from what doesn't by editing your budget, creative, placement options or audience."),
   ("Do you work with small businesses?","Yes. We offer a range of social media marketing packages for small and medium-sized businesses to suit your goals and budget."),
 ]),'svc_css.txt','sm_main.html')

# --- COPYWRITING ---
build(TPL,'service/copywriting/index.html',
 'Copywriting Services Sydney | SEO Copywriters &amp; Content | Online Consulting',
 'Professional website copywriting services in Sydney &mdash; SEO web copy, content strategy, eDMs and newsletters, blogs, resumes, annual reports and brochures.',
 BASE+'service/copywriting/',
 'Content &amp; Copywriting Sydney | Online Consulting',
 'Skilled SEO copywriters crafting content that ranks and converts &mdash; landing pages, eDMs, blogs and annual reports from an experienced Sydney team.',
 ld('Content & Copywriting','copywriting',
    'Professional website copywriting services in Sydney - SEO website copy, product content strategy, eDMs and newsletters, blog posts, resumes, annual reports and brochures.',
    'Copywriting',[
   ("What kinds of copy do you write?","From landing pages and electronic direct mail (eDMs) to blogs and annual reports - including SEO website copywriting, product content strategy, eDMs and newsletters, blog posts and articles, cover letters and resumes, and annual reports and brochures."),
   ("Is the copy written for search engines or for readers?","Both. Our web content copywriters are experts at pleasing search engines and customers, so you can rely on them to showcase the key features and benefits of your products or services. We also use SEO tools to increase organic traffic."),
   ("Can you help if I don't know what content I need?","Yes. We'll work with you to create a product content strategy tailor-made for your audience, then write to it."),
   ("Do you only write for new websites?","No. Whether you're looking to create a new website or hoping to update your existing one, we'll guide you through the process from start to finish."),
   ("Do I need a separate agency for the website itself?","No. We're a one-stop shop for all your needs, from web development and hosting, right through to adding copy to the pages."),
 ]),'svc_css.txt','cw_main.html')

# --- GOOGLE ADS ---
build(TPL,'service/google-adwords/index.html',
 'Google Ads Sydney | AdWords Management &amp; PPC Experts | Online Consulting',
 'Professional Google Ads (AdWords) services in Sydney from a Google Partner &mdash; PPC campaign setup, keyword targeting and careful budget management that drives results.',
 BASE+'service/google-adwords/',
 'Google Ads Sydney | Online Consulting',
 'Drive results with professional Google Ads services in Sydney. A Google Partner running PPC campaigns that win traffic, reach your audience and increase sales.',
 ld('Google Ads','google-adwords',
    'Google Ads (AdWords) management services in Sydney from a Google Partner - PPC campaign setup, keyword research, budget management and performance reporting.',
    'Pay Per Click Advertising',[
   ("How much do Google Ads cost?","It depends on what you're advertising. With Google Ads you only pay when someone clicks on your ad, and the cost per click varies depending on the keywords you target - some terms and industries are much more competitive than others. Management costs depend on your goals."),
   ("Is Google Ads the same thing as AdWords?","Yes - Google Ads was previously called AdWords. It's Google's pay-per-click (PPC) advertising platform, and you'll still see both names used."),
   ("What does a Google Partner mean for me?","As a Google Partner based on Sydney's Northern Beaches, we're Google Ads experts, and experts in understanding your needs to create optimised campaigns that drive revenue and results."),
   ("How do you decide which keywords to bid on?","As your AdWords service provider, we'll find the keywords your audience is using to find your product or services, handle your budget and align your campaigns to get the best results."),
   ("Should I run SEO at the same time?","It's usually worth it. We also offer SEO services and copywriting, so the keyword research done for your ads can feed the organic work as well."),
 ]),'svc_css.txt','ga_main.html')
