import os, re, glob, sys
from PIL import Image, ImageOps
SITE = os.path.expanduser('~/mnt/Version 2')
FI   = os.path.join(SITE, 'blog', 'featured-images')
TH   = os.path.join(FI, 'thumb')
os.makedirs(TH, exist_ok=True)
TW, THh = 860, 538
names = set()
for f in sorted(glob.glob(os.path.join(SITE, 'blog', '*.html'))):
    s = open(f, encoding='utf-8', errors='replace').read()
    m = re.search(r'featured-images/(?:thumb/)?([^"/]+)"', s) or re.search(r'<figure class="featured-image">\s*<img src="([^"]+)"', s)
    if m: names.add(os.path.basename(m.group(1)))
done = 0; skipped = 0; errs = []
budget = int(sys.argv[1]) if len(sys.argv) > 1 else 40
import time; t0 = time.time()
for n in sorted(names):
    out = os.path.join(TH, os.path.splitext(n)[0] + '.webp')
    if os.path.exists(out):
        skipped += 1; continue
    if time.time() - t0 > budget:
        break
    try:
        im = Image.open(os.path.join(FI, n))
        im = ImageOps.exif_transpose(im).convert('RGB')
        im = ImageOps.fit(im, (TW, THh), method=Image.LANCZOS, centering=(0.5, 0.42))
        im.save(out, 'WEBP', quality=80, method=5)
        done += 1
    except Exception as e:
        errs.append((n, str(e)))
print('total featured images:', len(names), '| made:', done, '| already there:', skipped,
      '| remaining:', len(names) - len(os.listdir(TH)))
if errs: print('ERRORS:', errs)
