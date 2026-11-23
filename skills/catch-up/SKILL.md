---
name: catch-up
description: This skill should be used when the user types "/catch-up", or says "catch me up", "I'm back on this project", "what happened while I was away", "brief me on the open PRs", "review the open PRs for me", or "I have no context on these PRs". It turns a repository's open pull requests into a local briefing page for a tech lead who does not read code, collects the lead's decisions, and turns them into PR comments. Works in any GitHub repository.
version: 0.1.0
---

# Catch-up: PR briefings for a tech lead who switches projects

The user is a tech lead who moves between projects. They know each project
well, but not the features the team built while they were away. They do not
read code; Claude's reviews cover the code. Their job is to understand each
feature and make the decisions only they can make.

The skill produces a local HTML page that groups open PRs by feature, gives
each feature its background first, shows the evidence, and asks the lead for
decisions. The lead exports the decisions, and Claude turns them into PR
comments.

## Principles

- **Context before evidence.** Every feature card and every decision starts
  with why the feature exists: the need, what people do today, where the
  request came from, why this design, and one concrete example. Without it the
  lead cannot decide. Do not explain the project itself; the lead knows it.
- **Features, not PRs.** Group stacked PRs (each based on the one below) and
  PRs that share an ADR or spec section into one feature card.
- **Evidence the lead can check without code:** behaviour (screenshots, staging),
  test promises mapped to rules, blocking findings verified at the head commit,
  and the 20 to 40 lines that matter.
- **Risk tiers set the depth.** Low: approve from the card. Medium: read the
  evidence. High: offer a walkthrough.
- **Plain English**, short sentences, no jargon without a meaning next to it.
  In conversation, one theme and one question at a time.
- **Never approve, merge or deploy.** Those need the lead's explicit go for each
  action, every time.

## State

Keep everything outside the repository, in
`~/Documents/catch-up/<repo-name>/`:

- `state.json`: `{ "lastRun": "YYYY-MM-DD", "decisions": { "<id>": {...} },
  "posted": [{ "pr": 974, "url": "...", "date": "..." }] }`
- `data-YYYY-MM-DD.json` and `catch-up-YYYY-MM-DD.html` for each run.
- `comments-YYYY-MM-DD.md` with the drafted PR comments.

Also save the lead's decisions as a project memory, so later sessions do not
ask the same questions.

## Workflow

### 1. Load what is known

1. Read the repository's CLAUDE.md files and the project memory.
2. Read `state.json` if it exists. The period starts at `lastRun`; on a first
   run, start 14 days back and say so.
3. Find the lead's GitHub login (`gh api user --jq .login`).

### 2. Gather the facts

Run these directly (they are quick):

- Open PRs: `gh pr list --limit 200 --json number,title,author,additions,deletions,createdAt,baseRefName,headRefName,isDraft,mergeable`
- Merged since the period start: `gh pr list --state merged --search "merged:>=<date>" --limit 200 --json number,title,author,mergedAt`
- Deploys: find the deploy workflows in `.github/workflows/` and list their
  recent runs with `gh run list --workflow <file>`. Note which commit runs in
  each environment, and how far main is ahead of production.
- New or changed ADRs and spec sections in the period.

### 3. Group into features

- Follow `baseRefName` chains: a PR whose base is another PR's head belongs to
  that stack. The stack's root is the PR based on `main`.
- Join PRs that cite the same ADR or spec section, or share a title prefix.
- Dependabot and small chores go to the "Other" list, not to a card.
- A feature with an earlier decision in `state.json` is a **follow-up**: its
  agent checks each item the lead asked for, and the card shows a follow-up
  block instead of a fresh briefing.

### 4. Fan out one agent per feature

Send all feature agents in one message, with the brief in
**`references/feature-agent-brief.md`**. Handle a feature of one small PR
inline instead of sending an agent. Tell the user how many agents run; they
see nothing until the agents finish.

### 5. Verify before writing

Agents can misread. Check these yourself before they reach the page:

- every claim about production or staging (what runs where, what a migration
  does there);
- every "blocking finding not fixed" and "CI never ran";
- every claim that the lead already approved or commented.

A claim that cannot be verified goes on the page as "not verified".

### 6. Build the page

1. Write `data-YYYY-MM-DD.json` in the shape in **`references/data-schema.md`**.
   - The summary: 3 to 5 lines, most important first, including production lag.
   - Decisions: only what the lead must decide. Typical sources: ADRs waiting
     for ratification, product rules a developer wrote into the spec, process
     conflicts (for example, a rule in CONTRIBUTING that PRs break), merge
     order between colliding PRs, production deploy lag.
   - Each decision gives context, one question, a clear recommendation and 2
     to 4 options, and names its feature.
2. Build: `python3 -I "${CLAUDE_SKILL_DIR}/scripts/build_page.py" <data.json> ~/Documents/catch-up/<repo>/catch-up-YYYY-MM-DD.html`
3. Check it renders: one headless Chrome `--dump-dom` run, counting the feature
   cards and the rendered mermaid SVGs. Then `open` the file.
4. Tell the user in a few lines what needs them most, and that the
   "Download decisions" button saves a JSON file to Downloads.

Use a local file, not a claude.ai artifact: the lead may use an account that
cannot open artifacts.

### 7. Turn decisions into comments

When the user gives the decisions file (in `~/Downloads/catch-up-decisions-*.json`):

1. Read it. A note in a decision is an instruction; "I want all tests covered"
   means every NO TEST row of that feature becomes a test request.
2. Write `comments-YYYY-MM-DD.md`: one comment per feature, on the root PR of
   its stack. Each comment lists what the developer must do before approval,
   the decisions for the record, and the tests to add. Write like a human: no
   em dashes, no filler, no bare `@login` mentions.
3. If a request conflicts with a design (for example, a guessable address on a
   page whose security depends on a secret address), stop and ask before
   drafting that part.
4. Show the drafts and wait for approval.
5. Post only if this project allows Claude to post GitHub comments (check the
   user's global instructions and the project memory; the default is no). If
   it does not, give the user the text to post.
6. Record what was posted in `state.json` and in the project memory.

### 8. Walkthroughs

When the lead asks for a walkthrough of a high-risk PR or ADR, go in parts:

1. The blocking findings, each as a short story with names ("Ana issues the
   link, then Bogdan ticks a private dinner"), the possible fixes, and a
   recommendation.
2. The most sensitive area (privacy, money, permissions), as questions with a
   recommendation each.
3. The open points or defaults, grouped in tables with "accept" or "change"
   per row; recommend changes only where they matter.

Ask after each part, explain any term the lead questions, and post the
decisions of each part to the PR before moving on.

### 9. Close the run

Update `state.json` (`lastRun`, decisions, posted comments). Tell the lead
what waits on developers, what waits on them, and that the next `/catch-up`
starts from today.

## Additional resources

- **`references/feature-agent-brief.md`**: the prompt for each feature agent.
- **`references/data-schema.md`**: the page data format and its rules.
- **`scripts/build_page.py`**: validates the data and builds the page.
- **`assets/template.html`**: the page template (light and dark, local
  storage, decision export, mermaid diagrams).
