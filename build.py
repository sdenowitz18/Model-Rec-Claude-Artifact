#!/usr/bin/env python3
"""Build the Model Match artifact.

Injects the embedded font CSS and the models.json snapshot into
src/template.html and writes the self-contained artifact to
dist/model-match.html.

To refresh the model data: replace models.json with a fresh export
(same shape, bump snapshotDate), then run  python3 build.py

Team-key build (zero-setup AI for teammates):
    MODEL_MATCH_API_KEY=sk-ant-... python3 build.py
Writes an ADDITIONAL file, dist/model-match-with-key.html, with the key
baked in so teammates get AI without pasting anything. That file is
git-ignored and must only be shared inside Transcend — anyone who has
the file can read the key, so use a spend-limited key.
"""
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent

template = (ROOT / "src" / "template.html").read_text()
fonts = (ROOT / "assets" / "fonts-inline.css").read_text()

snapshot = json.loads((ROOT / "models.json").read_text())
# compact + safe to embed inside a <script> block
models_js = json.dumps(snapshot, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")

base = template.replace("/*__FONTS__*/", fonts).replace("__MODELS_JSON__", models_js)

dist = ROOT / "dist"
dist.mkdir(exist_ok=True)

# Public build: no key baked in.
(dist / "model-match.html").write_text(base.replace("__TEAM_KEY__", ""))
print(f"dist/model-match.html — {len(base) // 1024} KB, {snapshot['modelCount']} models, snapshot {snapshot['snapshotDate']}")

# Optional internal build with the team key baked in.
key = os.environ.get("MODEL_MATCH_API_KEY", "").strip()
if key:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", key):
        sys.exit("MODEL_MATCH_API_KEY contains unexpected characters — refusing to embed it.")
    (dist / "model-match-with-key.html").write_text(base.replace("__TEAM_KEY__", key))
    print("dist/model-match-with-key.html — TEAM KEY EMBEDDED (git-ignored).")
    print("  Share this file only inside Transcend; anyone with the file can read the key.")
    print("  Use a spend-limited key from console.anthropic.com.")
