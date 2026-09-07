# -*- coding: utf-8 -*-
"""Formspree honours _next only on its paid plans; on the free plan a normal
POST lands on formspree.io/thanks. AJAX submission is available on every plan,
so post with fetch and do the redirect ourselves."""
import os, re, sys

ROOT = os.path.expanduser('~/mnt/public')
DRY  = '--apply' not in sys.argv

NEW_FN = '''window.ocRecaptchaSubmit = function (form) {
  var KEY = '6Lduh60tAAAAANnfWDZ9MOAYHkwvnPS6mDfkBvy1';

  /* Formspree only honours the _next field on its paid plans - on the free plan
     a plain POST lands on formspree.io/thanks and _next is ignored. Posting with
     fetch is available on every plan and answers with JSON, so the redirect is
     done here instead. _next is still submitted, so it takes back over
     untouched if the plan is ever upgraded. */
  function thanksUrl() {
    var n = form.querySelector('input[name="_next"]');
    return (n && n.value) || '/';
  }

  /* the book form has one foot per department, so target the open one */
  function foot() {
    return form.querySelector('.dept.is-active .form-foot')
        || form.querySelector('.ct-foot')
        || form.querySelector('.form-foot');
  }

  function errorBox() {
    var f = foot();
    if (!f) return null;
    var box = f.querySelector('.form-error');
    if (!box) {
      box = document.createElement('p');
      box.className = 'form-error';
      box.setAttribute('role', 'alert');
      f.insertBefore(box, f.firstChild);
    }
    return box;
  }

  function busy(on) {
    [].forEach.call(form.querySelectorAll('button[type="submit"]'), function (b) {
      b.disabled = on;
      b.setAttribute('aria-busy', on ? 'true' : 'false');
    });
  }

  function failed(msg) {
    busy(false);
    var box = errorBox();
    if (!box) return;
    box.textContent = msg || "We couldn't send that just now. Please try again, or call us on +61 2 8459 7882.";
    box.classList.add('is-on');
    try { box.scrollIntoView({ block: 'center', behavior: 'smooth' }); } catch (e) {}
  }

  function messageIn(data) {
    if (!data) return '';
    if (typeof data.error === 'string') return data.error;
    if (data.errors && data.errors.length) {
      return data.errors.map(function (e) { return e.message || ''; })
                        .filter(Boolean).join(' ');
    }
    return '';
  }

  function post() {
    var action = form.getAttribute('action');
    /* no fetch (or no action): fall back to the native POST, which at least
       still delivers the enquiry */
    if (!window.fetch || !window.FormData || !action) { form.submit(); return; }
    var box = errorBox();
    if (box) box.classList.remove('is-on');
    busy(true);
    /* FormData skips disabled fields, exactly like a native submit, so the
       departments the visitor did not pick stay out of it */
    fetch(action, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    }).then(function (res) {
      if (res.ok) { window.location.assign(thanksUrl()); return; }
      return res.json().then(function (d) { failed(messageIn(d)); },
                             function ()  { failed(''); });
    }, function () { failed(''); });
  }

  function send(token) {
    var f = form.querySelector('input[name="g-recaptcha-response"]');
    if (!f) {
      f = document.createElement('input');
      f.type = 'hidden';
      f.name = 'g-recaptcha-response';
      form.appendChild(f);
    }
    if (token) f.value = token;
    post();
  }

  if (typeof grecaptcha === 'undefined' || !grecaptcha.execute) { send(null); return; }
  try {
    grecaptcha.ready(function () {
      grecaptcha.execute(KEY, { action: 'submit' }).then(send, function () { send(null); });
    });
  } catch (err) { send(null); }
};
'''

CSS = ('.form-error{display:none;flex:1 0 100%;margin:0 0 6px;padding:12px 16px;'
       'border-radius:12px;background:#fdecec;box-shadow:inset 0 0 0 1px #f3c9c9;'
       'color:#8f1d1d;font-size:13.5px;line-height:1.55;}\n'
       '.form-error.is-on{display:block;}\n')

FN = re.compile(r'window\.ocRecaptchaSubmit = function \(form\) \{.*?\n\};\n', re.S)

anchors = {
    'book/index.html':    '.form-foot small{font-size:12.8px;color:var(--grey-light);}\n',
    'contact/index.html': '.ct-foot small{flex:1;min-width:220px;font-size:13px;color:var(--grey-light);line-height:1.6;}\n',
}

for rel, css_anchor in anchors.items():
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read()

    n = len(FN.findall(s))
    assert n == 1, '%s: found %d ocRecaptchaSubmit blocks' % (rel, n)
    s = FN.sub(lambda m: NEW_FN, s, count=1)

    if '.form-error{' not in s:
        assert css_anchor in s, '%s: css anchor missing' % rel
        s = s.replace(css_anchor, css_anchor + CSS, 1)

    if not DRY:
        open(p, 'w', encoding='utf-8', newline='').write(s)
    print('%s: fetch submit + error styling' % rel)

print('APPLIED' if not DRY else 'DRY RUN')
