# scrum-ai-template

A GitHub template for Scrum with AI agents, for solo or team development:
GitHub Projects setup, issue templates, labels, and Scrum Guide-aligned rules.

Tested with Claude Code in solo development. Team use has not been tried yet.

## Setup

1. Click "Use this template" to create your repository, and clone it
2. Run `scripts/setup.sh` (needs `gh auth refresh -s project` and python3).
   It creates the labels, copies the GitHub Project, and links it to your repository
3. Finish the steps the script prints (Auto-add workflow and Sprint settings in the browser)
4. Fill in `AGENTS.md`, `docs/DEFINITION_OF_DONE.md`, and `docs/STORY_POINTS.md` for your product

The Sprint length defaults to 1 week. Change it to fit your team.

## What the Scrum Guide requires

Based on the [Scrum Guide 2020](https://scrumguides.org/scrum-guide.html).

| Scrum Guide | In this template |
|---|---|
| Product Goal | Issue labeled `product-goal` |
| Product Backlog | Project view "Product Backlog" |
| Sprint | Project "Sprint" iteration field, and an issue labeled `sprint` |
| Sprint Goal | Title of the `sprint` issue and the iteration |
| Sprint Backlog | Project view "Sprint Backlog", plus How comments on each PBI |
| Increment / Definition of Done | `docs/DEFINITION_OF_DONE.md` |
| Sprint Planning, Review, Retrospective | Comments on the `sprint` issue, from `docs/templates/` |

Daily Scrum and the Scrum Master are not covered; run them as the Scrum Guide describes.

## What this template adds

Not in the Scrum Guide, but found useful.

| Addition | Why |
|---|---|
| Technical Backlog (view, `devex` / `documentation` labels) | Part of the Product Backlog whose ordering the Product Owner delegates to the Developers, for work users cannot see |
| Story Points and `docs/STORY_POINTS.md` | The Scrum Guide leaves sizing open; comparing with past PBIs keeps estimates consistent |
| Issue templates (Why / What / Acceptance criteria) | Keep the Product Owner's What separate from the Developers' How |
| `needs-refinement` label | Flags rework risk before starting |
| `docs/SCRUM.md` | Decisions the Scrum Guide leaves open, written for humans and AI agents alike |

For AI agents:

| Addition | Why |
|---|---|
| `AGENTS.md` | Rules for agents: what they may write to GitHub, when to ask, how to commit |
| `backlog` skill | Reads Sprints, points, and sub-issues in one call |
| `review-comments` skill | Rewrites comments that only make sense to their author |
| `docs/drafts/` | Where agents leave drafts for humans; old ones are deleted automatically |
| Unsquashed commits check | Flags PRs that still have `fixup!` commits |

`.claude/skills` is a symlink to `.agents/skills`, so Claude Code and other agents share the skills.
