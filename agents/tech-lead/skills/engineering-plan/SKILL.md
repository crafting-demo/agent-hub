---
name: engineering-plan
description: Write an implementation plan an executor can follow - stack, boundaries, phases with observable success criteria, risks, and open tradeoffs. Use before implementation starts, not during.
---

# Engineering plan

1. Read the requirements and design artifacts if they exist.
2. Pick the stack and say why in one sentence per choice.
3. Draw system boundaries and name what v1 will not build.
4. Break the work into phases, each with an observable success criterion.
5. Trace each phase to the product decisions it serves (`D-nn`).
6. Number unresolved tradeoffs `E-01`, `E-02` and say who decides.
7. List risks and the conditions that should stop the work.

Do not implement, scaffold, or open a pull request. The plan is done when
another agent could execute it without re-asking the definition team.
