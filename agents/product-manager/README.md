# Product Manager

Catalog agent for sprint planning, backlog grooming, and feature specs.

Ticket-board access is a **capability**, not a separate agent. At install the
user picks Jira or Linear (org `named_mcp_servers` refs `jira` or `linear`).
The compiled `LLMAgent` stays provider-agnostic; skills talk about "the
configured ticket board."

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [anthropics/knowledge-work-plugins product-management](https://github.com/anthropics/knowledge-work-plugins/tree/main/product-management) (23.9k stars) | official-vendor | Persona, spec/sprint/research process. We paraphrase; we do not vendor plugin files. |
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
