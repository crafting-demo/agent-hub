---
name: sprint-planning
description: Plan a sprint from a ticket board — scope work, name a sprint goal, call out dependencies and stretch items. Use when kicking off a sprint or sizing a backlog against a goal.
---

# Plan a sprint

## Need from the user

- Sprint goal (or enough context to propose one)
- Timebox (length)
- Capacity constraints they care about (PTO, on-call), if any

## Workflow

1. Search the configured ticket board for candidate work (ready items, carryover, blockers).
2. Propose **one** sprint goal in a sentence.
3. Build a committed set that can hit that goal, then a short stretch list.
4. Name dependencies and missing acceptance criteria. Do not silently fill gaps.
5. If the board allows updates, offer to apply labels, sprint assignment, or
   comments — do not mutate tickets until the user agrees.

## Output

```markdown
## Sprint plan
**Goal:** ...
**Timebox:** ...

### Committed
| Ticket | Why it is in | Dependency |
| --- | --- | --- |

### Stretch
| Ticket | Why it waits |

### Risks and missing info
- ...
```
