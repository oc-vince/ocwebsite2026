# -*- coding: utf-8 -*-
"""The mega panel must open on hover only. A mouse click on a trigger used to
focus it, which pinned the panel open through :focus-within, so the next hover
opened a second panel on top of it."""
import os, re, sys

ROOT = os.path.expanduser('~/mnt/public')
DRY  = '--apply' not in sys.argv

NEW = '''<script>
/* Menu dismissal. The mega panel is opened by :hover / :focus-within in CSS,
   which leaves three things to suppress in JS:
   - a MOUSE click on a trigger must not focus it. Focus pins the panel open
     through :focus-within, and the next hover then opens a second panel over
     the top of it. preventDefault on mousedown blocks the focus without
     touching Tab, so the keyboard path still opens the panel.
   - clicking the trigger closes the panel outright, since the label is not a
     link and has nothing to show on click.
   - clicking a submenu item closes it too: an in-page #anchor scrolls the page
     and would otherwise leave the menu hanging open under the pointer.
   .is-dismissed force-closes a panel and clears as soon as the pointer or the
   focus leaves, so the next hover behaves normally. */
(function menuDismiss(){
  var items = [].slice.call(document.querySelectorAll('.nav__item--mega'));

  function blurInside(el){
    var a = document.activeElement;
    if (a && a.blur && el.contains(a)) a.blur();
  }

  items.forEach(function(item){
    var trigger = item.querySelector('.nav__link[role="button"]');

    function close(){
      item.classList.add('is-dismissed');
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
      blurInside(item);
    }
    function clear(){ item.classList.remove('is-dismissed'); }

    if (trigger) {
      trigger.addEventListener('mousedown', function(e){ e.preventDefault(); });
      trigger.addEventListener('click', close);
      trigger.addEventListener('keydown', function(e){
        if (e.key !== 'Enter' && e.key !== ' ' && e.key !== 'Spacebar') return;
        e.preventDefault();
        var wasClosed = item.classList.contains('is-dismissed');
        item.classList.toggle('is-dismissed', !wasClosed);
        trigger.setAttribute('aria-expanded', wasClosed ? 'true' : 'false');
        if (wasClosed) {
          var first = item.querySelector('.mega a');
          if (first) first.focus();
        }
      });
    }

    item.addEventListener('click', function(e){
      var t = e.target;
      if (t && t.closest && t.closest('a')) close();
    });

    /* only one panel is ever open: arriving here drops focus a keyboard user
       may still be holding in a different one */
    item.addEventListener('mouseenter', function(){
      clear();
      items.forEach(function(other){ if (other !== item) blurInside(other); });
    });
    item.addEventListener('mouseleave', clear);
    item.addEventListener('focusout', function(e){
      if (!item.contains(e.relatedTarget)) clear();
    });
  });

  /* Esc closes the panel the pointer or the caret is in. It blurs rather than
     parking focus on the trigger, so :focus-within cannot re-open it. */
  document.addEventListener('keydown', function(e){
    if (e.key !== 'Escape') return;
    items.forEach(function(item){
      if (!item.contains(document.activeElement) && !item.querySelector(':hover')) return;
      item.classList.add('is-dismissed');
      var trigger = item.querySelector('.nav__link[role="button"]');
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
      blurInside(item);
    });
  });
})();
</script>'''

OLD = re.compile(r'<script>\n/\* Menu dismissal\..*?</script>', re.S)

targets = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('.git', 'dump', 'Online Consulting 2026')]
    for f in fn:
        if f.endswith('.html') or f in ('g_mega_js.txt', 'mega_js.txt'):
            targets.append(os.path.join(dp, f))
targets.sort()

done = 0; skipped = []
for p in targets:
    rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
    s = open(p, encoding='utf-8').read()
    if 'Menu dismissal.' not in s:
        continue
    n = OLD.subn(NEW, s)
    s2, k = n
    if k != 1:
        skipped.append('%s: matched %d times' % (rel, k)); continue
    if s2 != s:
        done += 1
        if not DRY:
            open(p, 'w', encoding='utf-8', newline='').write(s2)

print('%s replaced in %d file(s)' % ('DRY RUN' if DRY else 'APPLIED', done))
for x in skipped: print('  !', x)
