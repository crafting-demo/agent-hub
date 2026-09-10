# Engineering Manager

The engineering role in both phases. In **definition** mode it writes
`ENGINEERING.md` — stack and why, boundaries, phases traced to the product
decisions `D-nn`, open `E-nn` tradeoffs — and stops. In **delivery** mode it
plans the change and delegates to specialists. The same agent that planned the
work later gets it built.

Specialists are separate hub entries: `software-engineer`, `qa-engineer`, and
optionally `security-scanner`.

Cluster verification is not a separate specialist. When the template has a
Kubernetes intercept plan, this agent sends `qa-engineer` a second, separate
request for the cluster pass, so a fresh session grades it.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [google/adk-python](https://github.com/google/adk-python) SequentialAgent (21k stars) | popular-oss | Write-then-review sequence, no auto-refactorer |
| [Anthropic subagents](https://code.claude.com/docs/en/sub-agents) | official-vendor | Fresh verification session |
| [Get Shit Done](https://github.com/gsd-build/get-shit-done) (64.5k stars, archived) | popular-oss | Planner and roadmapper shape: opinionated stack, phases, traceability to locked decisions. Live successor: [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core). |
| [Anthropic best practices](https://code.claude.com/docs/en/best-practices) | official-vendor | Plan before code; keep planning out of the implementing session |

## Install

Create specialists first, then this agent. This coordinator carries no skills
and no CLI, so it stays stateless and Crafting can wire `sub_agents` on the
worker. It does take `transfer_to_workspace` so definition mode can write
`ENGINEERING.md`; that transfer is the last act of a definition session.
