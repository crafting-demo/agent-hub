# PDE Lead

Coordinator for the definition phase: product, design, engineering. Wired
sub-agents are `product-manager`, `design-lead`, and `engineering-manager` —
install all three before this agent. `engineering-manager` in turn needs its
own specialists, so an install of this coordinator pulls six agents.

Use it when the work is still "what are we building and how should it look,"
not "implement this issue." Delivery is a later `engineering-manager` session
on the same sandbox.

```
pde-lead ──> product-manager     ──> REQUIREMENTS.md (locked D-nn)
         ──> design-lead         ──> DESIGN.md
         ──> engineering-manager ──> ENGINEERING.md (phases, E-nn)
```

Two of the three do double duty: `product-manager` also runs a live ticket
board, and `engineering-manager` also delivers. Ask them to define, not
operate or deliver, and say so in the request.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [Get Shit Done](https://github.com/gsd-build/get-shit-done) (64.5k stars, archived) | popular-oss | Ask gray areas inline, lock numbered decisions before planning. Live successor: [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core). |
| [Anthropic subagents](https://code.claude.com/docs/en/sub-agents) | official-vendor | Specialists in isolated sessions; the coordinator sees summaries |

Process is paraphrased. We do not vendor GSD workflow files.
