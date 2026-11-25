---
name: review-comments
description: Reads the comments and docstrings added or changed in a diff as someone who does not know how the code came about, and rewrites the ones that do not make sense or are redundant. Use after implementing, before committing. Pass a git diff range (e.g. main...HEAD) to review that range, or file/directory paths to review every comment in them instead of a diff.
context: fork
agent: general-purpose
background: false
model: sonnet
---

# Review comments

The author knows the rejected alternatives and the words used in the conversation, so they tend to write
comments that assume them, and cannot notice it when rereading.
You do not know that history: read using only the code, and check that each comment makes sense.

## Target

What to review depends on whether "$ARGUMENTS" is paths or a git diff range.
Paths are one or more, separated by spaces. Treat an argument as a path if it exists relative to the repository root.

- Paths: every comment and docstring (including file headers) in each file, or in the git-tracked files of each directory.
  Used to review existing code. The "comments outside the diff" rule below does not apply; review every comment alike
- A range: `git diff` of that range. If empty, `git diff HEAD` plus untracked files from `git status --short`.
  Review the added or changed comments and docstrings (including file headers)
- When reviewing a diff, change a comment outside the diff only if it overlaps or contradicts one in the diff.
  If they overlap, do not keep both reworded: delete one, keeping the one in the place that fits the explanation
- To read without the history, do not read PRs, issues, or commit messages

If there are no comment changes in the diff, or no comments in the paths, do nothing and reply only "Nothing to review".

## What to look for

Read each comment alongside the code it explains, the file header and other comments in the same function,
and the definitions (and docstrings) of functions and constants it mentions.
Rewrite only what matches one of the points below. Leave everything else as written; do not change wording to taste.

### Does it make sense?

- It compares with something not in the code. "Does not add" — compared to what?
- It uses terms defined nowhere (shorthand from the author's head)
- It is far from the line it explains, so which line is unclear. Move it right above that line
- It says what, but not why. If the code already shows the what, delete it
- An object or the thing being compared is missing, so it is unclear what becomes what
- A word about position or relation reads two ways ("previous" in time or in order). Prefer the term
  the callee's docstring uses for the same thing
- A list in the comment (keys, formats, called functions) disagrees with the code.
  If the names are obvious from the code, drop the list and keep the point
- It breaks the project's comment rules, if the project has any (see `AGENTS.md`)

### Can the reader tell spec from reason from risk?

A sentence that only states a fact leaves the reader unsure whether it describes what the code does,
why it does it, or what goes wrong otherwise. Make it clear which one it is.

- Spec or procedure: leave as is
- Reason: connect it with "because" / "so that", so it is clear what it is the reason for
- Risk: say what goes wrong ("otherwise ...", "... would break")

If you cannot tell which one it is from the surrounding text and code, leave it and report it.

Bad:

```sh
# Always re-pull the base image. Cached layers do not get OS package updates.
docker build --pull .
```

Fixed:

```sh
# Always re-pull the base image; otherwise cached layers would miss OS package updates.
docker build --pull .
```

### Is it concise?

- It repeats the same thing in other words, within the comment or against nearby comments and names
- It has a preamble ("As a premise, ...") or a closing line ("This is a measure to prevent that")
- The reason includes history not needed to state the conclusion

Cut sentences without losing information (the why and the pitfalls).
When pointing to another comment to remove overlap, say what it points to so the sentence stands alone.

### When rewriting

- Keep it short. Do not write issue numbers
- Break lines at sentence or meaning boundaries, not at the full line width
- A docstring or file header that starts with a summary keeps the summary alone on the first line,
  unless the whole thing fits on one line
- A rewrite may be longer than the original only when the reader lacked needed information.
  Do not add what types, argument names, or nearby comments already say,
  nor words of degree or frequency (slightly, rarely, always) that neither the original nor the code has
- If you rename a term, check what that term means elsewhere in the file; do not use one word for two things
- Report, without changing code, problems that belong in names, function splits, or types
- Leave and report comments whose intent you cannot tell from the code.
  If a claim about behavior outside the code (libraries, browsers, Docker) looks doubtful, keep its content and report it

## Do not

- Change code (touch comments only)
- Commit

## Report

For each rewritten comment: file and line, which point it matched, and how it was fixed, in 1–2 lines.
When reviewing a diff, if you changed a comment outside the diff, say which comment in the diff it overlapped.
List separately the comments left because their intent was unclear, and those left because spec / reason / risk could not be told.
