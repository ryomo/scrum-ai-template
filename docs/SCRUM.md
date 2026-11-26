# Scrum Working Rules

Decisions on the parts of Scrum that are easy to get wrong or that the [Scrum Guide](https://scrumguides.org/scrum-guide.html) leaves open.
Sections marked **(supplement)** are not required by the Scrum Guide; they were added to make Scrum work on GitHub.

The Product Goal, Sprints, and Product Backlog items (PBIs) are managed in GitHub Projects.
The Sprint length and start day are written in the Project's README.

## Backlogs

| View | Shows issues labeled | Ordered by |
|---|---|---|
| Product Backlog | `enhancement` / `bug` | Product Owner |
| Technical Backlog | `documentation` / `devex` | Developers |
| Sprint Backlog | assigned to the current Sprint | Developers |

### Technical Backlog (supplement)

The Technical Backlog is **part of the Product Backlog, not a separate backlog**.
The Scrum Guide makes the Product Backlog the single source of work, ordered by the Product Owner, who may delegate that work.
Here the Product Owner delegates the ordering of work that users cannot see (developer experience, documentation) to the Developers.

It is a separate view so that whoever opens it knows at a glance whose list they are ordering.

Improvements from a Sprint Retrospective may also go straight into the next Sprint Backlog, as the Scrum Guide allows.

## Writing PBIs

### With an issue

Write Why / What / Acceptance criteria, using the templates in `.github/ISSUE_TEMPLATE/`.

The issue body (Why, What, Acceptance criteria, Out of scope) belongs to the Product Owner.
Developers do not add How to it. They write How as a comment on the issue,
or split it into sub-issues if it needs separate PRs.

How contains only the approach, why it was chosen over alternatives, and the pitfalls.
Leave out per-file steps, code snippets, and detailed API or DB shapes; the implementer decides those.
Aim for about 30 lines. If it gets longer, treat that as a sign to split into sub-issues rather than trimming.

If the PBI adds or changes UI, agree on its look before implementing:
make a mockup that opens in a browser and have the Product Owner check it.
Attach an image of the agreed mockup to a comment on the issue (e.g. `gh issue comment --attach`),
so that whoever implements it can see it.

If acceptance criteria or notes are added before implementation, re-estimate the Story Points.
If the scope grew a lot, split the added part into another PBI.
Do not adjust points after the work to match the actual effort.

### Story Points (supplement)

The Scrum Guide leaves sizing to the Developers without prescribing a method.
This template uses Story Points, estimated by comparing with the examples in [STORY_POINTS.md](STORY_POINTS.md).

### Sub-issues

- Set the Sprint on both the parent and the children. Otherwise the children do not appear in the Sprint Backlog
- Set Story Points on the parent only
- Give children the same type label as the parent. The backlog views filter by type label,
  so a different label puts the child in the other backlog
- Children are added to the Project automatically. Their status becomes Done when closed or when the linked PR is merged
- Close the parent after all children are closed and its acceptance criteria are met

### PRs without an issue

Skip the issue when writing it adds no information, for example:

- Typos and wording fixes
- An obvious bug fixed on the spot
- Cleanup that falls under an existing PBI's acceptance criteria

In that case, select the Project and Sprint in the PR's Projects field and enter Story Points,
so the PR appears in the Sprint Backlog.

### Issue conventions

- Titles are plain sentences. Do not prefix them with an area and a colon (`README: ...`)
- Record dependencies between issues as relationships (blocked by / blocking), not as text in the body
- Strike through checklist items that do not apply (`- [ ] ~~item~~`) instead of leaving them unchecked

## Labels

The meaning of each label is in its description on GitHub (source: `.github/labels.json`).
Only rules that a single label's description cannot express are written here.

- Every issue has exactly one type label: `bug` / `enhancement` / `documentation` / `devex`
- `needs-refinement` is used together with a type label. It only warns of rework risk;
  it does not decide whether the item may enter a Sprint. Refine the item before implementing it
- Issues closed without being done always get `wontfix`, so completed PBIs can be counted with `-label:wontfix`.
  Add `no:parent-issue` so sub-issues are not counted separately from their parent

## Product Goal

An issue labeled `product-goal`, with the goal itself as the title.
The Scrum Team fulfills (or abandons) one Product Goal before taking on the next.

## Sprint Goal

Write it as `Sprint N: <Sprint Goal>` in both the title of the `sprint` issue
and the title of the Iteration in the Project settings.
Iterations are added ahead of time titled just `Sprint N`; add the goal to the title at Sprint Planning.

The expected outcome describes only what users will be able to do, not how it will be built.

## Sprint Planning

Decide the Sprint Goal first, leading toward the Product Goal. Then select the PBIs within the capacity.
File the `sprint` issue once the goal is decided, and record the Planning as a comment on it,
copying the [template](templates/sprint-planning.md).

Then refine the selected PBIs as far as possible: update the body with the Product Owner if needed,
write How, and agree on the look of UI changes (see "Writing PBIs").
The Scrum Team may end Planning before all of them are refined; the rest are refined before each is implemented.
When Planning ends, update the record: fill in "Not yet refined", and the capacity if refinement changed the Story Points.

## Sprint Review

Try the Increment of the Sprint hands-on. Turn improvements into new PBIs or update existing ones.

Record it as a comment on the Sprint issue, copying the [template](templates/sprint-review.md),
and link the comment from the "Records" section of the issue body.

## Sprint Retrospective

Record it as a comment on the Sprint issue, copying the [template](templates/sprint-retrospective.md),
and link the comment from the "Records" section of the issue body.

Turn improvement actions into issues as needed. Actions not turned into issues stay in the record,
and their effect is checked at the next Retrospective.
Address the most impactful improvements as soon as possible.

## Ending a Sprint

Close the Sprint issue when its closing checklist (in `.github/ISSUE_TEMPLATE/sprint.md`) is complete.
Unfinished PBIs go back to the Product Backlog: set them to Todo and clear their Sprint.
