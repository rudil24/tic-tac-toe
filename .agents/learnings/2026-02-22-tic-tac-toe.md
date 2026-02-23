# Learnings: Tic-Tac-Toe

## Learning: Strict Adherence to Global Negative Rules

**ID**: L1  
**Category**: process  
**Confidence**: high  

### What We Learned

We must never offer ad-hoc editor configurations for IDEs that aren't Antigravity (e.g. changing `.vscode` or `pyrightconfig.json`). We must stick to native global Antigravity python environment solutions to fix diagnostic warnings, or accept failure modes cleanly if they appear to be backend issues.

### Why It Matters

Violating user-defined global negative rules causes severe friction, wastes time, and degrades trust with the agent.

### Source

Tic-Tac-Toe Python Linting Errors debugging session and Product Owner Feedback.

---

## Learning: Terminal Commands Safety and Initialization

**ID**: L2  
**Category**: tooling  
**Confidence**: high  

### What We Learned

Terminal executions often trigger "not allowed" errors from Antigravity safety prompts or macOS security restrictions. We also discovered we must rigorously follow setup workflows to avoid missing foundational steps like `git init`.

### Why It Matters

If we aren't careful about how terminal permissions affect our workflow, automated tasks will hang. Missing `git init` causes version control chaos.

### Source

Addressing "Fixing Terminal Permissions" during the Tic-Tac-Toe kickoff and deploying the setup scripts.

---

## Learning: Continuous Project Logging

**ID**: L3  
**Category**: process  
**Confidence**: high  

### What We Learned

We discovered the hard way that we should never skip updating `LOCAL_LOG.md` at the end of every phase. It's the only definitive local memory for tracking our continuous technical decisions.

### Why It Matters

Without a continuous log, the team loses context across stages (Scope, Design, Dev, Deploy), making retrospectives harder and losing valuable technical decisions.

### Source

Tic-Tac-Toe Team Retro feedback.

---

## Learning: 100% Test Coverage for Algorithmic Projects

**ID**: L4  
**Category**: testing  
**Confidence**: medium  

### What We Learned

Keeping test coverage at 100% natively using `pytest` for contained algorithmic projects made scaling the difficulty (adding the Minimax algorithm) effortless and safe.

### Why It Matters

Native testing removes the burden of manual QA, and provides the confidence to make sweeping logic refactors in core systems.

### Source

Tic-Tac-Toe core gameplay loop and Vera (QA) feedback.
