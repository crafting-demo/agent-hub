# Crafting Agent Hub

A catalog of ready-to-install AI agents for [Crafting](https://docs.sandboxes.cloud). Pick an agent, connect the tools it needs, and start working.

Every agent here has a defined role like Product Manager, Code Reviewer, Contract Analyst, etc. Personas skills, and tools are all sourced agents published by industry-leading companies.

Capabilities are defined as interfaces. A Product Manager needs "a ticket board"; at install time you choose whether that is Jira or Linear. Agents are not tightly coupled to their tools.

This repo is the source that Crafting's **Agents → Add Agent** flow reads. It is also usable directly from the command line with the `cs` CLI.

## What is in the catalog

### Product and engineering

| Agent | What it does | Tools it needs | Inspired by |
| --- | --- | --- | --- |
| **Product Manager** (`product-manager`) | Writes feature specs, plans sprints, grooms the backlog. Refuses to invent tickets or metrics. | Ticket board: **Jira or Linear** (MCP), chosen at install | Anthropic's [product-management plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/product-management) |
| **Engineering Manager** (`engineering-manager`) | Plans a change, delegates implementation and verification, loops on failures. Never writes code itself. | Sub-agents: Software Engineer, QA Engineer, optionally Security Scanner | Google ADK [SequentialAgent](https://github.com/google/adk-python) (write, then review), Anthropic [subagents](https://code.claude.com/docs/en/sub-agents) |
| **Software Engineer** (`software-engineer`) | Implements a specified change in a Crafting sandbox and reports what changed. Does not judge its own work. | Crafting sandbox | Anthropic [Claude Code best practices](https://code.claude.com/docs/en/best-practices), OpenAI [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) |
| **QA Engineer** (`qa-engineer`) | Verifies a change against running services in the sandbox, drives the real user flow, reports pass or fail. Does not patch. | Crafting sandbox, [Playwright](https://github.com/microsoft/playwright) for web UIs | Anthropic's "fresh session verifies" rule |
| **Code Reviewer** (`code-reviewer`) | Read-only review of a diff for quality, correctness, and defensive security. One Critical / Suggestions / Good practices report. | Crafting sandbox with the diff | Anthropic [pr-review-toolkit](https://github.com/anthropics/claude-code), GitHub Copilot [review-code](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/review-code), OWASP Top 10 |

### Security and operations

| Agent | What it does | Tools it needs | Inspired by |
| --- | --- | --- | --- |
| **Security Scanner** (`security-scanner`) | Scans a URL for web vulnerabilities and reports findings by severity, as feedback for a coding loop. No exploits. | **CLI**: [lonkero](https://github.com/bountyyfi/lonkero), installed automatically in the agent's sandbox | Crafting's demo-org `webscan` agent; OWASP Top 10 |
| **Incident Commander** (`incident-commander`) | Reproduces a symptom in a sandbox, optionally compares through cluster intercept, writes a diagnosis. Does not fix. | Crafting sandbox, `cs k8s intercept` when a plan exists | Anthropic reviewer contract ("report, do not edit") |

### Legal

| Agent | What it does | Tools it needs | Inspired by |
| --- | --- | --- | --- |
| **Legal Counsel** (`legal-counsel`) | Coordinates a contract or compliance review, fans out to the two specialists below, merges one memo with GREEN / YELLOW / RED flags. | Sub-agents: Contract Analyst, Compliance Reviewer. Optional document store (Box or Microsoft 365 MCP) | Anthropic's [legal plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/legal) and [claude-for-legal](https://github.com/anthropics/claude-for-legal) |
| **Contract Analyst** (`contract-analyst`) | Clause-by-clause review against your negotiation playbook. Flags deviations and proposes redline language. | Contract text or file; a playbook file | Anthropic legal plugin, `/review-contract` |
| **Compliance Reviewer** (`compliance-reviewer`) | Privacy and compliance check (GDPR, CCPA, DPA terms, breach notice, sub-processors) on a contract or initiative. | Contract text or file | Anthropic legal plugin, `/compliance-check` |

All legal output is a draft for attorney review. These agents assist with legal workflow; they do not give legal advice.

## How the agents work together

Single agents are the default. Some are designed to run as a team:

- **Secure delivery.** Engineering Manager asks Software Engineer to implement, QA Engineer to verify, then Security Scanner to scan the endpoints. Findings go back to the engineer until clean.
- **Vendor contract review.** Legal Counsel sends the same agreement to Contract Analyst and Compliance Reviewer, then merges one memo.
- **Backlog to reviewed change.** Product Manager writes the spec from the ticket board, Engineering Manager delivers it, Code Reviewer gates the diff.

Runnable versions of these teams, with install prompts and example tasks, live in [crafting-demo/agent-patterns](https://github.com/crafting-demo/agent-patterns).

## Where the definitions come from

Each agent's `manifest.yaml` lists its `sources`, and every source is one of:

- **An official vendor publication** — Anthropic's plugins and Claude Code docs, OpenAI's Codex guides, GitHub Copilot's prompt library, Google's ADK.
- **Widely adopted open source** — GitHub repositories with at least 10,000 stars (Playwright, Claude Code, Google ADK).
- **A published standard** — OWASP Top 10, CWE, the [Agent Skills](https://agentskills.io) format.

We paraphrase the published process into Crafting-shaped instructions. We do not copy other vendors' plugin files into this repo. The full attribution table is in [SOURCES.md](SOURCES.md); each agent's own `README.md` names its sources.

## Install an agent

The convenient way is to start a **new session** in Crafting Agent UI with the **default agent** (do not pick a custom agent) and paste a prompt like this:

```
Install the Product Manager agent from https://github.com/crafting-demo/agent-hub and follow INSTALL.md.
```

Swap in any catalog name (`Code Reviewer`, `Legal Counsel`, …). Coordinators also install their specialists. Name Linear instead of Jira if that is your ticket board. The default agent follows [INSTALL.md](INSTALL.md). After it finishes, start another **new** session and select the agent you just installed. Org admins get shared agents (`--shared`); otherwise the agent is personal.

You can also install by hand. You need the Crafting `cs` CLI, logged in to your org, and Python 3 with PyYAML.

```sh
git clone https://github.com/crafting-demo/agent-hub
cd agent-hub

# 1. Compile the package. For agents with a provider choice, pick one.
python3 scripts/build.py product-manager --provider ticket_board=jira

# 2. If the build produced a sandbox template, create it first.
cs template create hub-product-manager dist/product-manager/template.yaml

# 3. Create the agent (org-shared). Drop --shared for a personal agent.
cs llm agent create product-manager --shared dist/product-manager/agent.yaml
```

Then open Crafting Agent UI, start a new session, and select `product-manager`.

For a team, create the specialists before the coordinator (for example `software-engineer`, `qa-engineer`, `security-scanner`, then `engineering-manager`). Use `cs llm agent update` and `cs template update` if the names already exist.

Ticket-board access goes through the MCP servers your org admin has already approved (`named_mcp_servers`). No credentials live in this repo or in the compiled agent.

## What an agent package looks like

```
agents/product-manager/
  manifest.yaml       What it is, where it came from, what tools it needs,
                      what tasks to suggest. Read by the Add Agent UI.
  instructions.md     The persona. Plain Markdown.
  agent.yaml          Runtime wiring only (tools, sub-agents, model).
  skills/             Agent Skills (SKILL.md) the agent can draw on.
                      (Agents can also use skills defined inside working repos.)
  tools/              CLI installers and wrappers, where needed.
  README.md           Human-readable catalog page.
```

`scripts/build.py` compiles a package into exactly what Crafting already accepts: an `LLMAgent` YAML for `cs llm agent create`, plus a sandbox template when the agent needs skills or a CLI on disk. There are no new runtime fields. The compiled output is what you would have written by hand, generated from parts that are easier to review and reuse.

The full contract is in [SPEC.md](SPEC.md). `scripts/validate.sh` checks every manifest against the JSON Schema in `schema/` and runs `cs template validate` on generated templates.


## License

Original Crafting YAML, instructions, and skills in this repo are Apache-2.0. Upstream sources keep their own licenses; see each agent's `README.md`.
