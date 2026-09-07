import sys, os
sys.path.insert(0, os.path.expanduser('~/oc_build'))
from assemble import build
BASE='https://onlineconsulting.com.au/'
ORG={"@type":"Organization","name":"Online Consulting","url":BASE,"telephone":"+61 2 8459 7882",
     "address":{"@type":"PostalAddress","addressLocality":"Allambie Heights","addressRegion":"NSW","addressCountry":"AU"}}
ld={"@context":"https://schema.org","@graph":[
 {"@type":"ContactPage","name":"Contact Online Consulting","url":BASE+"contact.html",
  "description":"Contact Online Consulting - phone, email and our two Sydney offices in the CBD and on the Northern Beaches.","publisher":ORG},
 {"@type":"Organization","name":"OnlineConsulting.com.au Pty Ltd","url":BASE,
  "telephone":"+61 2 8459 7882","email":"info@onlineconsulting.com.au",
  "contactPoint":[{"@type":"ContactPoint","telephone":"+61 2 8459 7882","email":"info@onlineconsulting.com.au",
                   "contactType":"customer support","areaServed":"AU","availableLanguage":"English"}],
  "address":{"@type":"PostalAddress","streetAddress":"Level 2/35 Clarence St","addressLocality":"Sydney",
             "addressRegion":"NSW","postalCode":"2000","addressCountry":"AU"},
  "location":[
    {"@type":"Place","name":"Head Office","address":{"@type":"PostalAddress","streetAddress":"Level 2/35 Clarence St","addressLocality":"Sydney","addressRegion":"NSW","postalCode":"2000","addressCountry":"AU"}},
    {"@type":"Place","name":"Northern Beaches Studio","address":{"@type":"PostalAddress","streetAddress":"30 Smith Avenue","addressLocality":"Allambie Heights","addressRegion":"NSW","postalCode":"2100","addressCountry":"AU"}}]},
 {"@type":"BreadcrumbList","itemListElement":[
   {"@type":"ListItem","position":1,"name":"Home","item":BASE},
   {"@type":"ListItem","position":2,"name":"Contact","item":BASE+"contact.html"}]}]}
build('one-partner.html','contact.html',
 'Contact Us | Sydney CBD &amp; Northern Beaches | Online Consulting',
 'Contact Online Consulting &mdash; call +61 2 8459 7882, email info@onlineconsulting.com.au, or visit our Sydney CBD head office or Northern Beaches studio.',
 BASE+'contact.html','Contact Online Consulting',
 'Call, email or message us. Two Sydney offices &mdash; Level 2/35 Clarence St in the CBD and 30 Smith Avenue, Allambie Heights.',
 ld,'contact_css.txt','contact_main.html')
