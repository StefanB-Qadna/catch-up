# catch-up

A Claude Code skill for tech leads who move between projects.

Type `/catch-up` in a GitHub repository. Claude reads the open pull requests, groups them by feature, and builds a local HTML briefing page. Each feature card explains why the feature exists before it shows the evidence. The page asks you only for the decisions that need you. You export your decisions, and Claude drafts the PR comments from them.

Claude never approves, merges or deploys anything without your explicit go.

## Install

As a plugin (updates with `/plugin marketplace update`):

```
/plugin marketplace add StefanB-Qadna/catch-up
/plugin install catch-up@catch-up
```

As a plain skill in `~/.claude/skills`:

```sh
curl -fsSL https://raw.githubusercontent.com/StefanB-Qadna/catch-up/main/install.sh | bash
```

Restart Claude Code after either install.

## Requirements

- Claude Code
- `gh`, logged in to an account that can read the repository
- `python3`
- Google Chrome, optional, for the render check

## Use

1. Open Claude Code in a GitHub repository and type `/catch-up`.
2. Read the page that opens. Pick your decisions and click **Download decisions**.
3. Tell Claude the decisions file is ready. Claude drafts one comment per feature and waits for your approval.

Run state lives in `~/Documents/catch-up/<repo>/`, outside the repository. The next run starts from the date of the last one.

## Layout

- `skills/catch-up/SKILL.md`: the workflow
- `skills/catch-up/references/`: the brief for each feature agent and the page data schema
- `skills/catch-up/scripts/build_page.py`: checks the data and builds the page
- `skills/catch-up/assets/template.html`: the page template
