# Brief for one feature agent

Send one `general-purpose` agent per feature, all in one message so they run in
parallel. Fill in the angle-bracket parts. Keep the brief whole: the agent knows
only what it says.

---

You are gathering evidence for a tech lead who does not read code and who has
no context on this feature. Repository: <absolute repo path>. Read the root
CLAUDE.md and the CLAUDE.md of each directory the PRs touch first.

**Read-only.** Do not post anything to GitHub, do not push, do not change the
repository. Use `gh` and `git`.

Target: <feature name>, PRs <numbers in stack order>. Check each PR's base
branch to confirm the order.
<If an earlier run decided on this feature, paste the decisions and the
comments that were posted, and add: "Check each requested item against the
current head. Report done or not done for each, with evidence.">

Report FACTS with `file:line`. Mark anything you could not verify.

**A. Background (the most important part).**
1. The need in everyday words: who uses it and what problem it solves.
2. What people do today without it.
3. Where it came from: the PR's "Why" section, the client plan section, the
   ticket or task link and title, dates, who asked or who decided. Quote the
   source. If the source does not say who decided, say so.
4. Why this design, and the options the PR or ADR rejected.
5. One concrete example of a real user using it, step by step.
6. The terms a newcomer needs, each with a one-line meaning.

**B. Evidence, per PR.**
1. What it does in everyday words.
2. Architecture: new tables, migrations, routes, server actions, modules,
   external systems. Enough to draw a small box diagram.
3. Decision signals, each with `file:line`: a migration that changes existing
   data; a new dependency; a change to who may do what; a new path that writes
   to an external system, sends email or touches production data; a deviation
   from an ADR or the spec; a new pattern where the codebase already has one; a
   product rule the developer wrote into the spec.
4. Risk tier (low / medium / high) with a one-line reason. High means a
   migration on existing data, auth or roles, an external write, email,
   deletion or restore.
5. Test promises: the test names each PR adds. Map each rule the feature
   touches (spec rule IDs, ADR decisions, PR claims) to the test that proves
   it, or NO TEST.
6. Automated review: read issue comments and review comments. List each
   blocking finding and whether a later commit fixed it, verified at the head.
   Note any comment by the tech lead (<login>).
7. The PR's risk, rollback and follow-up sections, briefly. Flag them if empty
   on a risky PR.
8. CI status at the head (`gh pr checks`), merge state, days open. If the diff
   looks larger than the work, find out why.
9. For the riskiest PR: 2 or 3 sharp questions for the developer, and the
   20 to 40 lines that matter most (path, line range, two plain sentences).
10. Anything that looks wrong or needs the tech lead's decision.

Do not state a fact about production, staging or another PR without checking
it. Say "not verified" instead.

Return a compact markdown report in English, under 1,500 words. No filler.
