import sys, os
sys.path.insert(0, os.path.expanduser('~/oc_build'))
from assemble import build
ORG = {"@type":"Organization","name":"Online Consulting","url":"https://onlineconsulting.com.au/","telephone":"+61 2 8459 7882",
       "address":{"@type":"PostalAddress","addressLocality":"Allambie Heights","addressRegion":"NSW","addressCountry":"AU"}}
ld = {"@context":"https://schema.org","@graph":[
  {"@type":"AboutPage","name":"About Online Consulting",
   "url":"https://onlineconsulting.com.au/about.html",
   "description":"Online Consulting is a Sydney IT support company and digital agency founded by Sam Crawford in 2007 - IT, web and digital marketing under one roof.",
   "publisher":ORG},
  {"@type":"Organization","name":"Online Consulting","url":"https://onlineconsulting.com.au/",
   "foundingDate":"2007","telephone":"+61 2 8459 7882","email":"info@onlineconsulting.com.au",
   "founder":{"@type":"Person","name":"Sam Crawford"},
   "address":{"@type":"PostalAddress","streetAddress":"Level 2/35 Clarence St","addressLocality":"Sydney","addressRegion":"NSW","postalCode":"2000","addressCountry":"AU"},
   "areaServed":"Sydney, Australia"},
  {"@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://onlineconsulting.com.au/"},
    {"@type":"ListItem","position":2,"name":"About","item":"https://onlineconsulting.com.au/about.html"}]}
]}
build('one-partner.html','about.html',
  'About Us | Sydney IT Support Company &amp; Digital Agency Since 2007 | Online Consulting',
  'Online Consulting is a Sydney IT support company and digital agency founded in 2007 by Sam Crawford &mdash; IT support, web development and digital marketing under one roof.',
  'https://onlineconsulting.com.au/about.html',
  'About Online Consulting | Sydney IT &amp; Digital Agency',
  'Founded in 2007 on Sydney&#39;s Northern Beaches. A team of ICT experts covering IT support, web development and digital marketing &mdash; we make sense of the web.',
  ld, 'about_css.txt','about_main.html')
