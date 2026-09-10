# Install (read this first)

You are installing one or more catalog agents from this hub onto the **current org**. Follow this file until the agents exist and you have told the user which agent to select in a new session.

You have no extra context beyond this repository and tools available in this session (`cs` CLI after you are in a workspace).

## 1. Get this repository into a workspace

If the files of `https://github.com/crafting-demo/agent-hub` are **already** in the current workspace, use them. Do not clone again. If that directory is a git checkout of this repo, pull the latest default branch first so you install current files.

Otherwise:

1. Create a sandbox from this git repository (the URL the user pasted).
2. Target a workspace in that sandbox **immediately**. Do not stop to ask whether to open it.
3. Hand off to the workspace agent so you can run `cs` and `python3`.

This is an install, not an exploration. After the sandbox exists, keep going until the agents are created.

Work from the repository root (the directory that contains this `INSTALL.md`).

## 2. Choose shared vs personal agents

Prefer org-shared agents:

```sh
cs llm agent create NAME --shared FILE.yaml
```

If create fails because you are not an org admin, omit `--shared` (personal agents) and use the same omit on `update`.

If an agent already exists, update it instead of failing:

```sh
cs llm agent update NAME --shared FILE.yaml
```

Agent names are at most 20 characters: lowercase letters, digits, and dashes. Hub ids already satisfy that.

## 3. Which agent?

Read the user message. Map the name they used to a hub id:

| They said | Hub id |
| --- | --- |
| PDE Lead, product definition team | `pde-lead` |
| Requirements Lead | `requirements-lead` |
| Design Lead | `design-lead` |
| Tech Lead | `tech-lead` |
| Product Manager | `product-manager` |
| Engineering Manager | `engineering-manager` |
| Software Engineer | `software-engineer` |
| QA Engineer | `qa-engineer` |
| Integration Tester | `integration-tester` |
| Code Reviewer | `code-reviewer` |
| Security Scanner | `security-scanner` |
| Security Reviewer | `security-reviewer` |
| Incident Commander | `incident-commander` |
| Legal Counsel | `legal-counsel` |
| Contract Analyst | `contract-analyst` |
| Compliance Reviewer | `compliance-reviewer` |

If they asked for more than one, install each, specialists before coordinators (see below).

## 4. Compile and create

From the repository root, for each hub id `AGENT` (specialists first):

```sh
python3 scripts/build.py AGENT
```

**Provider choice.** If the user named a ticket board for Product Manager, pass it:

```sh
python3 scripts/build.py product-manager --provider ticket_board=jira
# or ticket_board=linear
```

If they did not name one, compile unbound (the agent still works from pasted tickets; MCP is not attached). Do not stop to ask.

If `dist/AGENT/template.yaml` exists, create or update the sandbox template **before** the agent:

```sh
cs template create hub-AGENT dist/AGENT/template.yaml \
  || cs template update hub-AGENT dist/AGENT/template.yaml
```

Then create or update the agent:

```sh
cs llm agent create AGENT --shared dist/AGENT/agent.yaml \
  || cs llm agent update AGENT --shared dist/AGENT/agent.yaml
```

### Specialists before coordinators

If the user asked for a coordinator, install its specialists first, then the coordinator.

- `pde-lead` needs `requirements-lead`, `design-lead`, `tech-lead`
- `engineering-manager` needs `software-engineer`, `qa-engineer`, `security-scanner`
- `legal-counsel` needs `contract-analyst`, `compliance-reviewer`

If they only asked for the coordinator, still install those specialists. Do not ask.

`integration-tester` is optional for `engineering-manager` and is not one of its sub-agents. Install it only when the user asks for cluster verification or says their templates have a Kubernetes intercept plan.

## 5. When you are done

Verify with `cs llm agent list` and `cs llm agent show AGENT --shared` (omit `--shared` if the agent is personal).

Tell the user:

- install is finished
- which agent to select in a **new** session
- for Product Manager, whether a ticket board was bound (Jira, Linear, or unbound)
- not to keep using this install session for real work
