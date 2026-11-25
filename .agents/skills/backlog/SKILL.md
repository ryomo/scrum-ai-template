---
name: backlog
description: Reads the backlog (GitHub Projects and issues). Use when asked "what is the current Sprint", "list the PBIs", "acceptance criteria of #N", "what's next", "the Product Goal", and to see Sprint progress or Story Points.
allowed-tools: Bash(./.agents/skills/backlog/backlog.py:*) Bash(gh:*)
---

# Read the backlog

The Product Goal, Sprints, and PBIs are in GitHub Projects, and the issues are in the repository.
Which Project and repository is set in `config.json` next to this file (written by `scripts/setup.sh`).

Read them with `backlog.py`. `gh project item-list` has Sprints and points but no parent/child relations,
and `gh issue list` is the opposite, so plain `gh` needs two calls joined together.
`backlog.py` gets both with one GraphQL query.

```bash
./.agents/skills/backlog/backlog.py            # current Sprint (default)
```

| Command | Output |
|---|---|
| `sprint` | PBIs in the current Sprint, weekdays left, points done (same as no argument) |
| `backlog` | Items with no Sprint that are not Done. Product and Technical Backlog together |
| `list [--all]` | All items. Done is excluded by default |
| `overview` | The Project's README and the list of Sprints |
| `show <N>` | Issue body (Why / What / Acceptance criteria / Out of scope) and comments |

Output is one item per line: `status points #number title`. Sub-issues hang under their parent with `└`.

```
WIP   5pt  #106  Sidebar sits too far from the body on 4K displays  [sub 0/2]
Todo    -  #117    └ Sidebar items stay right next to the body on wide screens
```

`[draft]` is an item not yet turned into an issue; it has no number, so it shows as `#-`.
`[PR]` is a PR filed without an issue. PRs share numbers with issues, so the mark tells them apart.

## Reading notes

- **Story Points are set on parent issues only.** A `-` on a sub-issue is not a missing estimate,
  and totals add up parents only
- Lists are ordered `WIP → Todo → Done`. Within a status, the Project's order (the priority) is kept
- A child whose parent is not listed appears alone with `[parent #N]` (e.g. only the parent is in the Sprint). That is normal

## Writing

**Write to the Project or issues (status, adding items, points, comments) only when told to**,
except for the How comment described in `AGENTS.md`. `backlog.py` is read-only; write with `gh` directly.

```bash
gh issue comment 106 --body-file <file>
```

- **Never reorder Project items.** The order is the Product Owner's (or Developers') priority
- Rules for filing issues, labels, and Sprint events are in `docs/SCRUM.md`

## Gotchas

- **The `gh` token needs the read/write `project` scope.** Without it `backlog.py` stops with `gh failed`.
  `gh auth refresh -s project` needs browser authentication, so **ask a human to run it**
- **`show` covers the issue only.** Sprint and points are Project fields and do not appear in
  `gh issue view`. Use `sprint` / `list` to see them
