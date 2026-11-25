# Definition of Done

The quality bar every Product Backlog item (PBI) must meet before it is Done.

<!--
Replace the examples with your project's own checks: commands, environments, and the kinds of change
that need extra care. Keep each item checkable. Move a recurring acceptance criterion here
once it applies to every PBI.
-->

## 1. It works

- [ ] All acceptance criteria in the issue are met
- [ ] Verified by actually running it in the local environment (e.g. `docker compose up -d`)
- [ ] Existing features are not broken (related screens and APIs were tried)

## 2. Code quality

- [ ] Type checks pass (e.g. `npx tsc --noEmit`)
- [ ] Formatters and linters leave no diff and no warnings (e.g. `npx eslint . --fix`)
- [ ] All existing automated tests pass (e.g. `npm test`)
- [ ] Logic that must not break (authorization, data migration, etc.) has unit tests for the change
- [ ] The author can explain the added or changed code in their own words,
  including code written by AI ("why is it like this?" has an answer)

## 3. Documentation

- [ ] `README.md` is updated if setup or startup changed

## 4. Pull Request

- [ ] Commits and the PR follow the rules in `AGENTS.md`

## Not part of the DoD

- Test coverage targets
- Performance tests
