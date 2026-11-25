# Development Guide

<!-- Describe the product, its structure, and the commands to run, test, and lint it. -->

Development follows Scrum. Working rules: `docs/SCRUM.md`. Definition of Done: `docs/DEFINITION_OF_DONE.md`.

## Backlog

The Product Goal, Sprints, and PBIs are managed in GitHub Projects. Read them with the `backlog` skill.

- Do not write to the Project or issues (adding items, changing status, commenting) without being told to,
  except for the How comment on a PBI (see below)
- Issues are added to the Project automatically; do not add them separately
- Never reorder Project items
- Iterations (Sprints) are added by a human in the Project settings. Adding them through the API
  renumbers existing iteration IDs and clears every item's Sprint

## Working on a PBI

- Before implementing:
  - Refine with the human and update the body if needed (always, if it has `needs-refinement`)
  - Post How as a comment on the issue without waiting for instructions
  - Get the human's approval to start implementing
- Before the PR: check off the met acceptance criteria and delete resolved "Open questions"

## Writing for humans

- When filing an issue, copy the template in `.github/ISSUE_TEMPLATE/`, fill it in, and keep its comments
- End PR, issue, and comment bodies written by an agent with `🤖 Generated with <agent name>`,
  so they can be told apart from human writing
- Put files for a human to check (drafts of issues, comments, PR bodies, alternatives to compare) in `docs/drafts/`
  and tell the human the path. Their contents are not committed, and old ones are deleted on branch switches.
  Temporary files the human does not need go in the session's own temporary directory

## Commits and PRs

- Work on a branch from main
- Commit messages are one line per issue, prefixed with `feat:` / `fix:` / `docs:` / `refactor:` etc.
  Reasons and `Closes #N` go in the PR body, not the commit message
- Write the PR body by copying `.github/pull_request_template.md` and following its comments
  (passing `--body-file` skips the template)
- Commit when implementation is done, even without being told.
  Before committing, review the comments in the diff with the `review-comments` skill
- Stack fixes after a human review with `git commit --fixup`.
  Squash with `git rebase --autosquash main` only when the human says so
- Uncommitted changes found when starting work are the human's edits.
  Review them and include them in the fixup; ask the human if something looks wrong
- Do not suppress static analysis or lint warnings (inline comments or config-wide).
  If the code cannot fix it, propose the suppression and let the human decide
