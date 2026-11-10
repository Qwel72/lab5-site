"""Ensure real linters reject broken fixtures, without changing published files."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
ROOT = Path(__file__).resolve().parents[1]
with TemporaryDirectory(prefix="orbita-ci-fixtures-") as tmp:
    tmp = Path(tmp)
    cases = [
        ("broken.html", '<!doctype html><html lang="ru"><head><title>Test</title></head><body><img src="x.jpg"></body></html>',
         "html-validate", ".htmlvalidate.json", "alt"),
        ("broken.css", ".example { colro: red; }", "stylelint", ".stylelintrc.json", "colro"),
    ]
    for name, text, tool, config, diagnostic in cases:
        path = tmp / name; path.write_text(text)
        result = subprocess.run([str(ROOT / "node_modules/.bin" / tool), "--config", str(ROOT / config), str(path)], cwd=ROOT, text=True, capture_output=True)
        output = result.stdout + result.stderr
        expected_code = 1 if tool == "html-validate" else 2
        assert result.returncode == expected_code, (tool, result.returncode, output)
        assert diagnostic in output, (tool, output)
        print(f"PASS: {tool} rejected intentionally broken {name}")
