---
name: lock-decisions
description: Turn a product brief and user answers into numbered locked decisions, deferred ideas, and open questions. Use in the definition phase, before anyone implements.
---

# Lock decisions

1. Separate what the user settled from what is still open.
2. Write settled items as `D-01`, `D-02`, … one sentence each, in the
   user's terms.
3. List deferred ideas explicitly so they cannot leak into v1.
4. List open questions that still block, and say who must answer.
5. Never silently assume an answer to an open question.

Downstream agents honor `D-nn` and do not re-ask. If new information
contradicts a locked decision, surface the conflict instead of quietly
changing it.
