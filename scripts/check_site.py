from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json, sys
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = []; self.links = []; self.images = []; self.h1 = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.append(a["id"])
        if tag == "h1": self.h1 += 1
        if tag == "img": self.images.append(a)
        for key in ("src", "href"):
            if a.get(key): self.links.append(a[key])
p = SiteParser(); p.feed((ROOT / "index.html").read_text())
assert p.h1 == 1, "Expected one h1"
assert len(p.ids) == len(set(p.ids)), "Duplicate IDs"
checked = 0
for value in p.links:
    u = urlsplit(value)
    if u.scheme or u.netloc: continue
    if not u.path and u.fragment:
        assert unquote(u.fragment) in p.ids, "Broken anchor: " + value
    if u.path:
        target = (ROOT / unquote(u.path)).resolve()
        assert target.is_relative_to(ROOT), "Path escapes site root"
        assert target.is_file(), "Missing local resource: " + value
    checked += 1
assert len(p.images) >= 3, "Expected at least three photographs"
for image in p.images:
    assert image.get("alt", "").strip(), "Missing descriptive alt"
    assert image["src"].startswith("images/"), "Photographs must be local"
    assert int(image.get("width", 0)) > 0 and int(image.get("height", 0)) > 0
text = (ROOT / "index.html").read_text()
assert "form-action 'none'" in text, "Demo form must not send data"
assert 'src="script.js" defer' in text, "Script must be deferred"
print(f"PASS: one h1, unique IDs, {checked} local references, {len(p.images)} photos, demo-form protections")
