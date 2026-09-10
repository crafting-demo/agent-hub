---
name: groom-backlog
description: Review a ticket-board backlog for unclear items, duplicates, missing acceptance criteria, and prioritization questions. Use when cleaning a backlog or preparing sprint planning.
---

# Groom a backlog

Read the configured board. Do not invent tickets.

## Check each item for

- Title and description a new engineer could implement from
- Acceptance criteria that can fail
- Duplicate or overlapping work
- Missing assignee, priority, or parent epic when the board uses those fields
- Hidden scope (open-ended "and also")

## Output

Group findings:

1. **Fix now** — specific edits (title, description, AC)
2. **Ask the user** — questions that change priority or scope
3. **Merge or close** — duplicates, with the surviving ticket id
4. **Ready** — items that can enter a sprint as-is

Propose edits; apply them only when asked.
