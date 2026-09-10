# PDE Lead

Coordinator for the definition phase: product, design, engineering. Wired
sub-agents are `requirements-lead`, `design-lead`, and `tech-lead` — install
all three before this agent.

Use it when the work is still "what are we building and how should it look,"
not "implement this issue." Delivery is a later `engineering-manager`
session on the same sandbox.

```
pde-lead ──> requirements-lead ──> REQUIREMENTS.md (locked D-nn)
         ──> design-lead       ──> DESIGN.md
         ──> tech-lead         ──> ENGINEERING.md (phases, E-nn)
```

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [Get Shit Done](https://github.com/gsd-build/get-shit-done) (64.5k stars, archived) | popular-oss | Ask gray areas inline, lock numbered decisions before planning. Live successor: [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core). |
| [Anthropic subagents](https://code.claude.com/docs/en/sub-agents) | official-vendor | Specialists in isolated sessions; the coordinator sees summaries |

Process is paraphrased. We do not vendor GSD workflow files.
