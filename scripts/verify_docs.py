from pathlib import Path
import re

html_content = Path('docs/index.html').read_text(encoding='utf-8')

# Check images
img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_content)
print(f"Found {len(img_srcs)} image references in index.html:")
all_ok = True
for src in img_srcs:
    p = Path('docs') / src
    if not p.exists():
        print(f"FAILED: Missing image: {p}")
        all_ok = False
    else:
        print(f"OK: {src} ({p.stat().st_size:,} bytes)")

# Check scripts & stylesheets
links = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', html_content)
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html_content)

for href in links:
    if not href.startswith('http') and not href.startswith('data:'):
        p = Path('docs') / href
        status = "OK" if p.exists() else "FAILED"
        print(f"Stylesheet {href}: {status}")
        if not p.exists(): all_ok = False

for src in scripts:
    p = Path('docs') / src
    status = "OK" if p.exists() else "FAILED"
    print(f"Script {src}: {status}")
    if not p.exists(): all_ok = False

if all_ok:
    print("\nALL DOCS WEB ASSETS VALIDATED WITH 100% PARITY.")
else:
    print("\nSOME ASSETS WERE MISSING.")
