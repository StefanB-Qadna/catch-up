# Catch-up page data schema

`scripts/build_page.py` reads one JSON file in this shape and injects it into
`assets/template.html`. The script refuses a file that misses a required field.

Fields marked **HTML** may hold simple inline HTML (`<strong>`, `<em>`, `<code>`).
Every other string is escaped. In any string, `#123` becomes a link to that PR.

```jsonc
{
  "meta": {
    "project": "my-app",            // required, repo name
    "date": "2026-11-16",                  // required, ISO date of this run
    "dateLabel": "16 Nov 2026",
    "repoUrl": "https://github.com/OWNER/REPO",  // required, no trailing slash
    "period": "Back on the project · 10–16 November"
  },
  "headline": "23 open PRs. 9 places need you.",
  "summary": ["4 to 5 lines, the TL;DR, most important first"],   // HTML
  "stats": [["23", "open PRs"], ["5", "features"]],
  "away": ["what merged, deployed or changed since the last run"], // HTML
  "callouts": ["a warning that spans features, e.g. two features easy to confuse"], // HTML

  "decisions": [{
    "id": "adr-0043",                      // required, stable across runs
    "feature": "sponsor",                  // id of the feature card it belongs to, or omit
    "tag": "ADR 0043 · #993",
    "tier": "high",                        // required: low | med | high
    "title": "A private page for each sponsor",
    "context": "2-3 lines, plain words",   // required, HTML
    "question": "Do you ratify the ADR now?",
    "rec": "<strong>Not yet.</strong> why", // required, HTML
    "options": ["Ratify", "Ratify after X", "Reject"],
    "sub": ["detail question"]             // HTML, optional
  }],

  "features": [{
    "id": "sponsor",                       // required, stable across runs
    "name": "Private sponsor page",
    "tier": "high",
    "who": "author · 3 PRs · open 3 days",
    "plain": "what it does, in everyday words",
    "background": {                        // required for every feature
      "need": "the problem",
      "today": "what people do without it",
      "origin": "client plan section, ticket, date, who asked",
      "why": "why this design",
      "story": "a concrete example of someone using it",
      "terms": [["Term", "meaning"]],
      "unsure": "what the sources do not say, e.g. who decided"
    },
    "followUp": {                          // only when an earlier run decided on this feature
      "since": "16 Nov",
      "items": [[true, "rebased #980, CI green"], [false, "no screenshots yet"]]
    },
    "verdict": "where it stands, one or two sentences",
    "evidence": [["ok|gap|bad", "Claude review", "detail"]],
    "diagram": "flowchart LR\n  A[Page] --> B[(table)]",  // mermaid, optional
    "signals": ["decisions hidden in the code"],          // HTML
    "tests": [["promise", "test name", true], ["promise", null, false]],
    "lines": [["path/file.ts:10-40", "what these lines decide"]],
    "questions": ["question for the developer"],
    "prs": [[993, "what it does", "high"]],                // required
    "actions": ["Approve", "Send the questions", "I want a walkthrough", "Block"]
  }],

  "chores": [["#1015", "Node 26 in CI", "yours, green, ready to merge"]],
  "notes": ["how the page was made and what was not checked"]
}
```

## Rules

- Keep `id` values stable between runs (`adr-0043`, `rooms`), so a follow-up run
  can match earlier decisions to the same item.
- Every decision that belongs to a feature names it in `feature`. The page then
  shows the feature's background inside the decision.
- `tests` rows with `covered: false` render as **NO TEST** in red. Never mark a
  promise covered without a test name.
- The export button writes `catch-up-decisions-<project>-<date>.json` to the
  user's Downloads folder, with the PR numbers of each feature.
