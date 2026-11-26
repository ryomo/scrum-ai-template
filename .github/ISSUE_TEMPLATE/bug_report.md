---
name: Bug report
about: Report something that does not work as expected
title: ''
labels: 'bug'
---

<!--
A defect found in work still in progress in the current Sprint is not filed here.
Move that item back to "Todo" or "In Progress" instead.
-->

<!--
The title describes the symptom.
  Good: The first character typed with an IME disappears right after opening a note
  Bad:  IME issues
-->

<!--
Do not write How (implementation) here. Developers write it as an issue comment or sub-issues
during or after Sprint Planning.
-->

## Why

<!--
What the symptom keeps users from doing.

Example:
Users have to retype every time they start writing, which gets in the way of writing itself.
There is no workaround, so creating a new note is broken for everyone.
-->

## Symptom and steps to reproduce

<!--
Steps, actual result, expected result, environment, frequency.
If it cannot be reproduced, add "identify the conditions" to Open questions.

Example:
1. Open any note
2. Without clicking the body, type "a" with an IME

Actual:   the character disappears without showing candidates
Expected: candidates appear and input can be confirmed as usual

Environment: browser / OS, if it depends on them
Frequency: every time
-->

## What

<!--
One line on the state that should hold, not how to fix it.

Example:
IME input works normally right after opening a note.
-->

## Acceptance criteria

<!--
- The symptom does not appear when following the steps above
- What must be confirmed as not broken by the fix
- Make each line a checkbox (`- [ ]`)
- Do not repeat conditions already in docs/DEFINITION_OF_DONE.md, unless this PBI needs a different condition

Example:
- Characters do not disappear with the steps above
- Existing behavior of non-IME input and paste does not change
-->

- [ ]

## Out of scope

<!--
What was decided not to do this time. May be empty.

Example:
- Misplaced candidate window
- A general review of IME handling
-->

## Open questions

<!--
What is not yet decided or confirmed. May be empty. Delete each item once resolved.
While anything remains here, keep the `needs-refinement` label.

Example:
- Not yet checked whether it reproduces in other browsers
- Whether the same cause affects other inputs (the title field)
-->
