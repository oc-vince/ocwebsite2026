# -*- coding: utf-8 -*-
"""Book page: drop the three AI options from IT Support, add an Other option
with a required detail box, and rename every field's `name` to the question the
visitor actually read, so the Formspree email is legible."""
import os, re, html, sys

ROOT = os.path.expanduser('~/mnt/public')
DRY  = '--apply' not in sys.argv
BOOK = os.path.join(ROOT, 'book/index.html')

def norm(t):
    t = re.sub(r'<em class="req">\*</em>', '', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    for a, b in (('’', "'"), ('‘', "'"), ('“', '"'),
                 ('”', '"'), ('–', '-'), ('—', '-'), ('…', '')):
        t = t.replace(a, b)
    t = re.sub(r'\s+', ' ', t).strip()
    return t.rstrip(' *:').strip()

s = open(BOOK, encoding='utf-8').read()

# ---------- 1. remove the three AI options ----------
for v in ('Build AI agents and intelligent solutions',
          'Adopt AI across my organisation',
          'AI automation'):
    block = ('        <label class="choice">\n'
             '          <input type="checkbox" name="it_goals[]" value="%s">\n'
             '          <span class="box" aria-hidden="true"></span>\n'
             '          <span class="t">%s</span>\n'
             '        </label>\n' % (v, v))
    assert s.count(block) == 1, 'AI option not found verbatim: ' + v
    s = s.replace(block, '', 1)
print('removed 3 AI options')

# ---------- 2. add Other + its reveal field ----------
last = ('        <label class="choice">\n'
        '          <input type="checkbox" name="it_goals[]" value="Find a Virtual Assistant">\n'
        '          <span class="box" aria-hidden="true"></span>\n'
        '          <span class="t">Find a Virtual Assistant</span>\n'
        '        </label>\n'
        '      </div>\n'
        '    </div>\n')
assert s.count(last) == 1, 'IT goals tail not found'
new = ('        <label class="choice">\n'
       '          <input type="checkbox" name="it_goals[]" value="Find a Virtual Assistant">\n'
       '          <span class="box" aria-hidden="true"></span>\n'
       '          <span class="t">Find a Virtual Assistant</span>\n'
       '        </label>\n'
       '        <label class="choice">\n'
       '          <input type="checkbox" name="it_goals[]" value="Other">\n'
       '          <span class="box" aria-hidden="true"></span>\n'
       '          <span class="t">Other</span>\n'
       '        </label>\n'
       '      </div>\n'
       '      <div class="reveal-field" id="it-other-field">\n'
       '        <label class="field">\n'
       '          <span>Please tell us what you need <em class="req">*</em></span>\n'
       '          <input type="text" name="it_goals_other" required disabled>\n'
       '        </label>\n'
       '      </div>\n'
       '    </div>\n')
s = s.replace(last, new, 1)
print('added Other option + required detail box')

# ---------- 3. derive name -> question label ----------
form = s[s.index('<form id="bookForm"'):s.index('</form>', s.index('<form id="bookForm"'))]
tokens = re.finditer(
    r'(?P<h4><h4>.*?</h4>)'
    r'|(?P<pq><p class="q">(?P<q>.*?)</p>)'
    r'|(?P<consent><div class="consent">)'
    r'|(?P<fspan><label class="field">\s*<span[^>]*>(?P<sp>.*?)</span>)'
    r'|(?P<field><(?:input|select|textarea)\b[^>]*name="(?P<name>[^"]+)"[^>]*>)',
    form, re.S)

h4 = pq = span = None
in_consent = False
labels, order = {}, []
for m in tokens:
    if m.group('h4'):
        h4 = norm(m.group('h4')); pq = span = None; in_consent = False
    elif m.group('pq'):
        pq = norm(m.group('q')); span = None; in_consent = False
    elif m.group('consent'):
        in_consent = True
    elif m.group('fspan'):
        span = norm(m.group('sp'))
    else:
        n = m.group('name')
        if n.startswith('_') or n == 'department':
            continue
        if in_consent:
            lbl = 'Consent'
        elif n.endswith('[]') or span is None:
            # an h4 phrased as a question IS the question; a <p class="q"> that
            # follows one is only a "choose one" style instruction
            lbl = h4 if (h4 and h4.endswith('?')) else (pq or h4)
        else:
            lbl = span
        if n not in labels:
            labels[n] = lbl; order.append(n)

labels['department_label'] = 'Department'
for n in order:
    assert labels[n], 'no label derived for ' + n

# ---------- 4. apply the renames, keeping a stable data-key for the JS ----------
def rename(m):
    tag, n = m.group(0), m.group('name')
    if n not in labels:
        return tag
    key = n[:-2] if n.endswith('[]') else n
    new_name = labels[n] + ('[]' if n.endswith('[]') else '')
    tag = tag.replace('name="%s"' % n, 'data-key="%s" name="%s"' % (key, new_name), 1)
    return tag

head, body = s[:s.index('<form id="bookForm"')], s[s.index('<form id="bookForm"'):]
end = body.index('</form>')
body = (re.sub(r'<(?:input|select|textarea)\b[^>]*name="(?P<name>[^"]+)"[^>]*>',
               rename, body[:end]) + body[end:])
s = head + body

# the hidden department input duplicated the select; keep the id for the JS but
# stop it posting a second identical line
s = s.replace('<input type="hidden" name="department" id="deptValue" value="">',
              '<input type="hidden" id="deptValue" value="">', 1)
print('renamed %d fields' % len(labels))

# ---------- 5. JS: key off data-key, and re-apply conditionals after show() ----------
old_js = """  /* conditional: current website URL */
  form.addEventListener('change', function(e){
    var t = e.target;
    if (t.name === 'wd_haswebsite') {
      var box = document.getElementById('wd-url-field');
      var open = (t.value === 'Yes');
      box.classList.toggle('is-open', open);
      var input = box.querySelector('input');
      input.disabled = !open;
    }
    if (t.name === 'vp_purpose[]' && t.value === 'Other') {
      var vbox = document.getElementById('vp-other-field');
      vbox.classList.toggle('is-open', t.checked);
      var vinput = vbox.querySelector('input');
      vinput.disabled = !t.checked;
      if (t.checked) vinput.focus();
    }
    if (/_(date|time|method|consent)$/.test(t.name || '')) markStep(3);
  });"""
new_js = """  /* Conditional fields. Every field posts under the question the visitor read,
     so the JS keys off data-key instead of name. A reveal field stays disabled
     while hidden, which is what stops the required input inside it from
     blocking validation. */
  function setReveal(boxId, on, focus){
    var box = document.getElementById(boxId);
    if (!box) return;
    box.classList.toggle('is-open', on);
    var f = box.querySelectorAll('input, select, textarea');
    [].forEach.call(f, function(el){
      el.disabled = !on;
      if (!on) el.value = '';
    });
    if (on && focus && f.length) f[0].focus();
  }

  /* show() re-enables everything in the active panel, hidden reveal fields
     included, so their state has to be put back straight afterwards */
  function syncReveals(){
    function isOn(key, val){
      var el = form.querySelector('[data-key="' + key + '"][value="' + val + '"]');
      return !!el && el.checked;
    }
    setReveal('wd-url-field',   isOn('wd_haswebsite', 'Yes'),   false);
    setReveal('vp-other-field', isOn('vp_purpose',    'Other'), false);
    setReveal('it-other-field', isOn('it_goals',      'Other'), false);
  }

  form.addEventListener('change', function(e){
    var t = e.target, k = t.getAttribute('data-key');
    if (k === 'wd_haswebsite') setReveal('wd-url-field', t.value === 'Yes', false);
    if (k === 'vp_purpose' && t.value === 'Other') setReveal('vp-other-field', t.checked, true);
    if (k === 'it_goals'    && t.value === 'Other') setReveal('it-other-field', t.checked, true);
    if (/_(date|time|method|consent)$/.test(k || '')) markStep(3);
  });"""
assert s.count(old_js) == 1, 'conditional JS block not found'
s = s.replace(old_js, new_js, 1)

old_show = """    markStep(2);

    if (typeof ScrollTrigger !== 'undefined')"""
new_show = """    markStep(2);
    syncReveals();

    if (typeof ScrollTrigger !== 'undefined')"""
assert s.count(old_show) == 1, 'show() anchor not found'
s = s.replace(old_show, new_show, 1)
print('JS rewired to data-key, reveal state re-synced after show()')

if not DRY:
    open(BOOK, 'w', encoding='utf-8', newline='').write(s)

print('\n--- field name map ---')
for n in order:
    print('  %-20s -> %s' % (n, labels[n]))
print('\n%s' % ('DRY RUN' if DRY else 'APPLIED'))
