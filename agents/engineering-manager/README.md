# Engineering Manager

Coordinator for implementation plus verification. Specialists are separate
hub entries: `software-engineer`, `qa-engineer`, and optionally
`security-scanner`.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [google/adk-python](https://github.com/google/adk-python) SequentialAgent (21k stars) | popular-oss | Write-then-review sequence, no auto-refactorer |
| [Anthropic subagents](https://code.claude.com/docs/en/sub-agents) | official-vendor | Fresh verification session |

## Install

Create specialists first, then this agent. This coordinator is stateless
(no skills, no CLI) so Crafting can wire `sub_agents` on the worker.
