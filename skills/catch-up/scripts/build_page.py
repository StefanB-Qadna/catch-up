#!/usr/bin/env python3
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"
TIERS = {"low", "med", "high"}
EVIDENCE_KINDS = {"ok", "gap", "bad"}


def fail(msg):
    sys.exit(f"build_page: {msg}")


def check(data):
    meta = data.get("meta") or fail("missing meta")
    for key in ("project", "date", "repoUrl"):
        if not meta.get(key):
            fail(f"meta.{key} is required")
    feature_ids = set()
    for f in data.get("features", []):
        for key in ("id", "name", "tier", "plain", "verdict", "prs"):
            if key not in f:
                fail(f"feature {f.get('id', '?')}: {key} is required")
        if f["tier"] not in TIERS:
            fail(f"feature {f['id']}: tier must be one of {sorted(TIERS)}")
        if f["id"] in feature_ids:
            fail(f"duplicate feature id {f['id']}")
        feature_ids.add(f["id"])
        bg = f.get("background")
        if bg:
            for key in ("need", "today", "origin", "why"):
                if not bg.get(key):
                    fail(f"feature {f['id']}: background.{key} is required")
        for ev in f.get("evidence", []):
            if len(ev) != 3 or ev[0] not in EVIDENCE_KINDS:
                fail(f"feature {f['id']}: evidence rows are [ok|gap|bad, title, detail]")
        for t in f.get("tests", []):
            if len(t) != 3:
                fail(f"feature {f['id']}: test rows are [promise, test name or null, covered bool]")
    seen = set()
    for d in data.get("decisions", []):
        for key in ("id", "title", "tier", "context", "question", "rec", "options"):
            if key not in d:
                fail(f"decision {d.get('id', '?')}: {key} is required")
        if d["id"] in seen:
            fail(f"duplicate decision id {d['id']}")
        seen.add(d["id"])
        if d.get("feature") and d["feature"] not in feature_ids:
            fail(f"decision {d['id']}: feature {d['feature']} does not exist")


def main():
    if len(sys.argv) != 3:
        fail("usage: build_page.py <data.json> <out.html>")
    data = json.loads(Path(sys.argv[1]).read_text())
    check(data)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = f"{data['meta']['project']} catch-up"
    html = TEMPLATE.read_text().replace("__TITLE__", title).replace("__DATA__", payload)
    out = Path(sys.argv[2]).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(out)


if __name__ == "__main__":
    main()
