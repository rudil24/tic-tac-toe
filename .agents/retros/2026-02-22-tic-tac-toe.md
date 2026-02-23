# Retrospective: Tic-Tac-Toe

**Date:** 2026-02-22
**Scope:** Initial scaffold, logic programming, linting debug, and agent interactions.

## Summary

The Tic-Tac-Toe project implementation was a success overall. The core game loop, test coverage, and progressive AI logic (Easy Random -> Hard Minimax) came together cleanly. However, breaking global user rules regarding editor configuration during debugging caused significant friction, prompting major process updates for future projects.

## What Went Well

- Project scaffolded quickly using project-kickoff and standard docs.
- Game logic and progressive AI implemented cleanly.
- 100% test coverage (`pytest`) made adding complexity completely safe and effortless.

## What Could Be Improved

- Absolute adherence to global rules: The team failed to respect the negative constraint against mentioning ".vscode" or other IDEs.
  - rudil24: it wasn't really mentioning it that was setting me off, it was the agent making changes to .vscode configs thinking it would fix antigravity is why I was so frustrated.
- `LOCAL_LOG.md` tracking: The team failed to update the continuous log during the deploy/retro stage initially.
- We must remember to do `git init` natively during setup (which has now been automated).

## Learnings Extracted

- L1: Strict Adherence to Global Negative Rules
- L2: Terminal Commands Safety and Initialization
- L3: Continuous Project Logging
- L4: 100% Test Coverage for Algorithmic Projects

See: `docs/learnings/2026-02-22-tic-tac-toe.md`

## Action Items

- [x] Create `ai-logic.md` synopsis of the Minimax implementation.
- [x] Update project setup scripts to strictly enforce `git init`.
- [x] Update `GLOBAL_EVOLUTION.md` to formally adopt Cap persona and update Retro rules.
