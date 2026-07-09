import json, re

SRC = "/root/.claude/projects/-home-user-Model-Rec-Claude-Artifact/45957acd-d7a6-555e-8a68-fe016769be31/tool-results/mcp-Airtable-list_records_for_table-1783626612842.txt"
OUT = "/home/user/Model-Rec-Claude-Artifact/models.json"

F = {
  "name": "fld75W7CFd9bI93Hw",
  "org": "fld58tXC5LkXKogBp",
  "website": "fldKnnqbVwUcuFF7D",
  "description": "fldCG9NGRsI1GI6wg",
  "grades": "fldkGYm7lY5nmA7EJ",
  "cost": "fldXisczjGdwgpMjK",
  "activities": "fldnWpPlvaRxIZO3U",
  "gradAims": "fldwifzdg3UnxF7Lf",
  "leaps": "fldE0kUa9htmZC2nV",
  "status": "fldda9ph1Q9N1Hgda",
  "topics": "fldcvVNJnmr8c1FL3",
  "reach": "fldjpiIpWNEJjJ2nG",
  "impact": "fld3XuVhXxwgndxP2",
}

def names(v):
    if not v: return []
    out = []
    for x in v:
        n = (x.get("name") or "").strip()
        if n and n != "-": out.append(n)
    # dedupe preserving order (Math appears twice in topic choices)
    seen = set(); res = []
    for n in out:
        if n not in seen: seen.add(n); res.append(n)
    return res

def clean_text(s, cap=900):
    if not s: return ""
    s = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", s)  # strip md links
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s).strip()
    if s in ("-", "- None found for solution", "None found for solution"): return ""
    if len(s) > cap: s = s[:cap].rsplit(" ", 1)[0] + "…"
    return s

data = json.load(open(SRC))
models = []
for r in data["records"]:
    c = r["cellValuesByFieldId"]
    if not c.get(F["activities"]): continue  # fully coded records only
    acts = names(c.get(F["activities"]))
    if not acts: continue
    m = {
        "id": r["id"],
        "name": (c.get(F["name"]) or "").strip(),
        "org": (c.get(F["org"]) or "").strip(),
        "website": (c.get(F["website"]) or "").strip(),
        "description": clean_text(c.get(F["description"]), 900),
        "grades": names(c.get(F["grades"])),
        "cost": names(c.get(F["cost"])),
        "activities": acts,
        "gradAims": names(c.get(F["gradAims"])),
        "leaps": [n.replace("ARCHIVE ", "") for n in names(c.get(F["leaps"])) if not n.startswith("ARCHIVE")],
        "topics": names(c.get(F["topics"])),
        "status": names(c.get(F["status"])),
        "reach": clean_text(c.get(F["reach"]), 400),
        "impact": clean_text(c.get(F["impact"]), 500),
    }
    if not m["name"]: continue
    models.append(m)

models.sort(key=lambda m: m["name"].lower())
snapshot = {
    "snapshotDate": "2026-07-09",
    "source": "Transcend research database (Airtable · All Solutions, fully coded records)",
    "modelCount": len(models),
    "models": models,
}
json.dump(snapshot, open(OUT, "w"), indent=1, ensure_ascii=False)
print(len(models), "models")
import os; print(os.path.getsize(OUT)//1024, "KB")
# taxonomy coverage
from collections import Counter
for k in ["grades","cost","activities","gradAims","leaps","topics"]:
    have = sum(1 for m in models if m[k])
    print(f"{k}: {have}/{len(models)}")
