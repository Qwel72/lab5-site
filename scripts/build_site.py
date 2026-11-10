from pathlib import Path
import json, os, shutil
from datetime import datetime, timezone
root = Path(__file__).resolve().parents[1]
out = root / "_site"
if out.exists():
    shutil.rmtree(out)
out.mkdir()
for name in ("index.html", "styles.css", "script.js", ".nojekyll"):
    shutil.copy2(root / name, out / name)
(out / "images").mkdir()
for src in sorted((root / "images").glob("*.jpg")):
    shutil.copy2(src, out / "images" / src.name)
revision = {"commit": os.environ.get("GITHUB_SHA", "local-check"),
            "run_id": os.environ.get("GITHUB_RUN_ID", "local"),
            "built_at": datetime.now(timezone.utc).isoformat()}
(out / "deployment.json").write_text(json.dumps(revision, indent=2) + "\n")
print("Static site prepared: HTML, CSS, JS, 3 photographs and deployment.json")
