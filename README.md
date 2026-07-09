# Model Match

A thought partner for Transcend teammates supporting communities through school
design work. Describe what a community is designing toward — five quick taps
plus your own words — and Model Match surfaces the learning models from
Transcend's research database worth a look, with transparent evidence for why.

**One self-contained file.** `dist/model-match.html` embeds the model data, the
brand fonts, and all logic. It runs anywhere a browser runs and is published as
a Claude artifact for org-wide sharing.

## How it works

- **Deterministic matching** computes the match matrix — which of the
  teammate's intake selections (grades, grad aims, Leaps, experiences, cost)
  each model hits or misses. This is verifiable evidence straight from the
  database tags, never AI-generated.
- **AI reasoning** (`window.claude.complete`, available when the file is
  opened as a Claude artifact) reads the teammate's freeform description,
  re-ranks the pre-screened shortlist, and writes the three design-specific
  reasons, honest considerations, and the "how these three differ" line. It can
  only choose from and cite the pre-screened database records.
- **Graceful fallback**: outside an AI-enabled context, ranking and the match
  matrix still work; reasons are built from tags alone and the tool says so.

## Repo layout

| Path | What it is |
|---|---|
| `models.json` | Snapshot of the research database (the only file to refresh) |
| `src/template.html` | The app — UI, matching engine, AI prompts |
| `assets/fonts-inline.css` | Bebas Neue + Open Sans embedded as data URIs |
| `build.py` | Injects fonts + data into the template → `dist/model-match.html` |
| `scripts-extract-from-airtable.py` | Reference script used to produce `models.json` from an Airtable export |
| `dist/model-match.html` | The built, shareable artifact |

## Refreshing the model data

1. Export the fully coded records (those with Activities tagged) from the
   **All Solutions** table in the Airtable research base into `models.json`,
   keeping the same shape:

   ```json
   {
     "snapshotDate": "YYYY-MM-DD",
     "source": "…",
     "modelCount": 111,
     "models": [
       {
         "id": "rec…", "name": "…", "org": "…", "website": "…",
         "description": "…",
         "grades": ["9","10"], "cost": ["Free"],
         "activities": ["…"], "gradAims": ["…"], "leaps": ["…"],
         "topics": ["CCL"], "status": ["Documented"],
         "reach": "…", "impact": "…"
       }
     ]
   }
   ```

2. Bump `snapshotDate`.
3. Run `python3 build.py`.
4. Re-publish `dist/model-match.html`.

The intake options, model counts, and snapshot date shown in the tool all
derive from `models.json` at runtime — no code changes needed for a refresh.

## Scope

**v1 (built):** arrive → structured intake with freeform → top-3 cards with
match matrix → runners-up → "show me 3 more" with rejection signal → refine →
copy-out for Slack/Notion → print view → feedback affordance → honest weak-fit
and drop-off states → clarifying questions when input is thin.

**Fast-follow (UI accommodates, not yet built):**
compare-two side-by-side, browse-all directory. (The ask-a-model chat drawer shipped in v1.1 — every recommended model has an "Ask AI" button opening a chat grounded only in that model's record.) The screen router, embedded
catalog, and card components are shared, so these slot in without a redesign.
