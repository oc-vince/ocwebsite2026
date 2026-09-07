# -*- coding: utf-8 -*-
"""Add invisible reCAPTCHA v3 to the booking and contact forms.

Flow: our own validation runs first. When the form is valid we ask Google for a
score token, drop it into the field Formspree looks for (g-recaptcha-response),
then call form.submit() -- a native submit, which deliberately skips the submit
listeners so we can't loop. If Google's script is blocked or errors we submit
anyway rather than leaving the visitor stuck on a dead button.
"""
import os, re

SITE_KEY = '6Lduh60tAAAAANnfWDZ9MOAYHkwvnPS6mDfkBvy1'

HELPER = '''
<!-- reCAPTCHA v3 (invisible, score-based). Badge is hidden, so the disclosure
     text next to each submit button is required by Google's terms. -->
<script src="https://www.google.com/recaptcha/api.js?render=%s"></script>
<script>
window.ocRecaptchaSubmit = function (form) {
  var KEY = '%s';
  function send(token) {
    var f = form.querySelector('input[name="g-recaptcha-response"]');
    if (!f) {
      f = document.createElement('input');
      f.type = 'hidden';
      f.name = 'g-recaptcha-response';
      form.appendChild(f);
    }
    if (token) f.value = token;
    form.submit();   /* native submit: bypasses the submit listeners above */
  }
  if (typeof grecaptcha === 'undefined' || !grecaptcha.execute) { send(null); return; }
  try {
    grecaptcha.ready(function () {
      grecaptcha.execute(KEY, { action: 'submit' }).then(send, function () { send(null); });
    });
  } catch (err) { send(null); }
};
</script>
''' % (SITE_KEY, SITE_KEY)

BADGE_CSS = '''.grecaptcha-badge{visibility:hidden;}
.rc-note{font-size:12px;color:var(--grey-light);line-height:1.55;}
.rc-note a{color:var(--grey);text-decoration:underline;text-underline-offset:2px;}
.rc-note a:hover{color:var(--blue);}
'''

NOTE = ('<small class="rc-note">Protected by reCAPTCHA &mdash; Google\'s '
        '<a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Privacy Policy</a> and '
        '<a href="https://policies.google.com/terms" target="_blank" rel="noopener">Terms of Service</a> apply.</small>')

def add_common(s):
    i = s.rindex('</style>')
    s = s[:i] + BADGE_CSS + s[i:]
    i = s.rindex('</body>')
    return s[:i] + HELPER + s[i:]

# ---------------- book ----------------
p = 'book/index.html'; s = open(p, encoding='utf-8').read()
assert 'ocRecaptchaSubmit' not in s
s = add_common(s)

OLD = '''    markStep(3);
  });'''
NEW = '''    /* valid: get a reCAPTCHA token, then submit for real */
    e.preventDefault();
    markStep(3);
    window.ocRecaptchaSubmit(form);
  });'''
assert s.count(OLD) == 1, s.count(OLD)
s = s.replace(OLD, NEW, 1)

OLD_FOOT = '''        <small>We reply within 2 business hours. No obligation, no sales script.</small>
'''
NEW_FOOT = OLD_FOOT + '        ' + NOTE + '\n'
n = s.count(OLD_FOOT)
assert n == 4, n
s = s.replace(OLD_FOOT, NEW_FOOT)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('book/index.html: reCAPTCHA wired, %d disclosure notes' % n)

# ---------------- contact ----------------
p = 'contact/index.html'; s = open(p, encoding='utf-8').read()
assert 'ocRecaptchaSubmit' not in s
s = add_common(s)

OLD = '''    /* Valid — let the browser POST to Formspree, which redirects to _next. */
'''
NEW = '''    /* Valid: get a reCAPTCHA token, then submit for real. */
    e.preventDefault();
    window.ocRecaptchaSubmit(form);
'''
assert s.count(OLD) == 1
s = s.replace(OLD, NEW, 1)

OLD_FOOT = '''            <small>We'll only use your details to reply to this enquiry. No lists, no sharing.</small>
'''
NEW_FOOT = OLD_FOOT + '            ' + NOTE + '\n'
assert s.count(OLD_FOOT) == 1
s = s.replace(OLD_FOOT, NEW_FOOT, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('contact/index.html: reCAPTCHA wired, 1 disclosure note')
