#!/usr/bin/env python3
"""Build the Model Match artifact.

Injects the embedded font CSS and the models.json snapshot into
src/template.html and writes the self-contained artifact to
dist/model-match.html.

To refresh the model data: replace models.json with a fresh export
(same shape, bump snapshotDate), then run  python3 build.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent

template = (ROOT / "src" / "template.html").read_text()
fonts = (ROOT / "assets" / "fonts-inline.css").read_text()

snapshot = json.loads((ROOT / "models.json").read_text())
# compact + safe to embed inside a <script> block
models_js = json.dumps(snapshot, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")

out = template.replace("/*__FONTS__*/", fonts).replace("__MODELS_JSON__", models_js)

dist = ROOT / "dist"
dist.mkdir(exist_ok=True)
(dist / "model-match.html").write_text(out)
print(f"dist/model-match.html — {len(out) // 1024} KB, {snapshot['modelCount']} models, snapshot {snapshot['snapshotDate']}")
