# -*- coding: utf-8 -*-
"""Top-level nav labels become non-clickable triggers, and the mega / mobile
   menus close when a submenu item is clicked."""
import os, re, sys

ROOT = os.path.expanduser('~/mnt/public')
DRY  = '--apply' not in sys.argv

NAV_A = re.compile(
    r'<a class="nav__link" href="[^"]*">(?P<label>.*?)</a>', re.S)

CSS_ANCHOR = ('.nav__item--mega:hover .mega,\n'
              '.nav__item--mega:focus-within .mega'
              '{opacity:1;visibility:visible;pointer-events:auto;}')

CSS_ADD = CSS_ANCHOR + """
/* the top-level labels are triggers, not links */
.nav__link[role="button"]{cursor:default;-webkit-user-select:none;user-select:none;
  -webkit-tap-highlight-color:transparent;}
/* clicking a submenu item force-closes the panel, so a same-page #anchor link
   does not leave the mega sitting open under the cursor */
.nav__item--mega.is-dismissed .mega{opacity:0!important;visibility:hidden!important;
  pointer-events:none!important;}
.nav__item--mega.is-dismissed .mega__panel{transform:translateY(-14px) scale(.985)!important;
  opacity:0!important;}"""

JS_ADD = """
<script>
/* Menu dismissal. The mega panel is hover/focus driven in CSS, so clicking an
   in-page #anchor would scroll the page and leave the panel open under the
   pointer. A one-shot .is-dismissed class closes it; it clears as soon as the
   pointer or focus leaves, so the next hover opens normally. */
(function menuDismiss(){
  var items = [].slice.call(document.querySelectorAll('.nav__item--mega'));

  items.forEach(function(item){
    function close(){
      item.classList.add('is-dismissed');
      var a = document.activeElement;
      if (a && a.blur && item.contains(a)) a.blur();
    }
    function clear(){ item.classList.remove('is-dismissed'); }

    item.addEventListener('click', function(e){
      var t = e.target;
      if (t && t.closest && t.closest('a')) close();
    });
    item.addEventListener('mouseleave', clear);
    item.addEventListener('focusout', function(e){
      if (!item.contains(e.relatedTarget)) clear();
    });

    /* the trigger is a span, so wire up the keyboard equivalent of a click */
    var btn = item.querySelector('.nav__link[role="button"]');
    if (btn) {
      btn.addEventListener('keydown', function(e){
        if (e.key !== 'Enter' && e.key !== ' ' && e.key !== 'Spacebar') return;
        e.preventDefault();
        var wasClosed = item.classList.contains('is-dismissed');
        item.classList.toggle('is-dismissed', !wasClosed);
        btn.setAttribute('aria-expanded', wasClosed ? 'true' : 'false');
        if (wasClosed) {
          var first = item.querySelector('.mega a');
          if (first) first.focus();
        }
      });
    }
  });

  document.addEventListener('keydown', function(e){
    if (e.key !== 'Escape') return;
    items.forEach(function(item){
      if (!item.contains(document.activeElement) && !item.querySelector(':hover')) return;
      item.classList.add('is-dismissed');
      var btn = item.querySelector('.nav__link[role="button"]');
      if (btn) { btn.setAttribute('aria-expanded', 'false'); btn.focus(); }
    });
  });
})();
</script>
<script>
/* Mobile menu: tapping any link inside it closes the panel, including #anchors
   on the current page where no navigation happens. */
(function mmenuDismiss(){
  var menu   = document.getElementById('mobileMenu');
  var burger = document.getElementById('burger');
  if (!menu || !burger) return;
  menu.addEventListener('click', function(e){
    var t = e.target;
    var a = t && t.closest ? t.closest('a') : null;
    if (!a || !menu.contains(a)) return;
    menu.classList.remove('is-open');
    burger.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    if (window.__lenis) window.__lenis.start();
    menu.querySelectorAll('.mmenu__group.is-open').forEach(function(g){
      g.classList.remove('is-open');
      var tog = g.querySelector('.mmenu__toggle');
      var sub = g.querySelector('.mmenu__sub');
      if (tog) tog.setAttribute('aria-expanded', 'false');
      if (sub) sub.style.maxHeight = '0px';
    });
  });
})();
</script>"""

def nav_sub(m):
    label = m.group('label')
    return ('<span class="nav__link" role="button" tabindex="0" '
            'aria-haspopup="true" aria-expanded="false">%s</span>' % label)

files = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('_tools', '.git', 'dump')]
    for f in fn:
        if f.endswith('.html'):
            files.append(os.path.join(dp, f))
files.sort()

stat = {'nav': 0, 'css': 0, 'js': 0, 'files': 0}
miss = []
for p in files:
    rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
    s = o = open(p, encoding='utf-8').read()

    s, n = NAV_A.subn(nav_sub, s)
    if n: stat['nav'] += n
    if n != 5: miss.append('%s: %d nav links converted (expected 5)' % (rel, n))

    if 'is-dismissed' not in s:
        if CSS_ANCHOR in s:
            s = s.replace(CSS_ANCHOR, CSS_ADD, 1); stat['css'] += 1
        else:
            miss.append('%s: CSS anchor not found' % rel)

    if 'menuDismiss' not in s:
        i = s.find('(function megaMenu(){')
        j = s.find('</script>', i) if i != -1 else -1
        if j != -1:
            j += len('</script>')
            s = s[:j] + JS_ADD + s[j:]; stat['js'] += 1
        else:
            miss.append('%s: megaMenu script not found' % rel)

    if s != o:
        stat['files'] += 1
        if not DRY:
            open(p, 'w', encoding='utf-8', newline='').write(s)

print('%s files=%d touched=%d nav=%d css=%d js=%d'
      % ('DRY RUN' if DRY else 'APPLIED', len(files), stat['files'],
         stat['nav'], stat['css'], stat['js']))
if miss:
    print('\nissues (%d):' % len(miss))
    for x in miss[:20]: print('  ', x)
