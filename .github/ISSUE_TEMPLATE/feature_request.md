---
name: Feature request
about: A change, functional or non-functional
title: ''
labels: 'enhancement'
---

<!--
The title alone should tell what this PBI changes.
Long titles are cut off in lists, so put the thing that changes (screen or feature name) first,
and make the whole title a summary of the change.
  Good: Search the body of saved notes / Sort the note list by last updated
  Bad:  Search improvements
-->

<!--
To choose the type label, see the table in "Backlogs" in docs/SCRUM.md.
-->

<!--
Do not write How (implementation) here. Developers write it as an issue comment or sub-issues
during or after Sprint Planning.
-->

## Why

<!--
Whose problem it is, and what gets better when it is solved.

Functional example:
As users' notes pile up, they have to scroll the sidebar endlessly to open the one they want.
Without remembering the title they cannot find it, and a note they cannot find is as good as lost.
We want users to reach a note from a fragment of its body.

Non-functional example:
Users with more than 1,000 notes keep reporting that the app takes over 10 seconds to start.
The wait makes it useless for jotting down ideas quickly.
-->

## What

<!--
The state that should hold, not the means.

Functional example:
Users can search the body of saved notes and open a matching note.

Non-functional example:
Startup time stays practical as the number of notes grows.

If it adds or changes UI, you may attach a mockup image here if you have one.
Either way, the look is agreed on with a mockup before implementation.
-->

## Acceptance criteria

<!--
Conditions that, once met, mean this PBI is satisfied.
- Write them so that anyone can tell from outside whether they are met
- Put numbers on non-functional criteria, and also state what must not get worse
- Make each line a checkbox (`- [ ]`)
- Do not repeat conditions already in docs/DEFINITION_OF_DONE.md, unless this PBI needs a different condition

Functional example:
- Typing a search term shows the notes whose body matches
- Selecting a result opens that note
- When nothing matches, a message says so
- Search is case-insensitive
- With 200 notes, results appear within 1 second

Non-functional example:
- With 2,000 notes, the app is ready for input within 2 seconds of starting
- With 10 notes, startup is not slower than now
- The measurement procedure is kept in the repository
-->

- [ ]

## Out of scope

<!--
What was decided not to do this time. May be empty.

Functional example:
- Sorting search results
- Saving search history
-->

## Open questions

<!--
What is not yet decided. May be empty. Delete each item once resolved.
While anything remains here, keep the `needs-refinement` label.

Functional example:
- Should file names be searched too, or ship body-only first?
- Show snippets around matches? Can that be a separate PBI?
-->
