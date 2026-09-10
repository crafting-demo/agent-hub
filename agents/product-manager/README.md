# Product Manager

Catalog agent for the product role in both phases: writing requirements and
specs when there is nothing yet, and planning sprints, grooming, and
clarifying tickets once there is a board.

Definition and operation are two modes of one agent, not two agents. With no
board bound it works from a brief and produces `REQUIREMENTS.md` with
numbered `D-nn` locked decisions — the artifact `pde-lead` fans out for. With
a board bound it also plans sprints and grooms the backlog.

Ticket-board access is a **capability**, not a separate agent. At install the
user picks Jira or Linear (org `named_mcp_servers` refs `jira` or `linear`).
The compiled `LLMAgent` stays provider-agnostic; skills talk about "the
configured ticket board."

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [anthropics/knowledge-work-plugins product-management](https://github.com/anthropics/knowledge-work-plugins/tree/main/product-management) (23.9k stars) | official-vendor | Persona, spec/sprint/research process. We paraphrase; we do not vendor plugin files. |
| [Get Shit Done](https://github.com/gsd-build/get-shit-done) (64.5k stars, archived) | popular-oss | Locked `D-nn` decisions, deferred ideas, discuss-then-plan order. Live successor: [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core). |
| [Agent Skills](https://agentskills.io/specification) | standard | `SKILL.md` layout |

## Capabilities

| Capability | Required | Providers |
| --- | --- | --- |
| `ticket_board` | yes | MCP `jira`, MCP `linear` |

`tool_mapping` is a starting map to common Atlassian and Linear MCP tool names.
Confirm against the live server during onboarding verification.

## Install

```sh
python3 scripts/build.py product-manager --provider ticket_board=jira
cs template create hub-product-manager dist/product-manager/template.yaml
cs llm agent create product-manager --shared dist/product-manager/agent.yaml
```

Use `ticket_board=linear` for Linear. The template is required because this
package ships skills.
