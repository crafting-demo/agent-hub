# Agent Hub package specification

Schema version: `0.1`

This document is the contract for entries in this hub. A package is metadata plus
files that **compile** into Crafting's existing runtime types. The runtime does
not grow new fields.

Compiled artifacts:

| Artifact | Crafting command | When |
| --- | --- | --- |
| `dist/<id>/agent.yaml` | `cs llm agent create <id> [--shared] FILE` | Always |
| `dist/<id>/template.yaml` | `cs template create hub-<id> FILE` then `cs template validate FILE` | Package has `skills/` or a `cli` provider |

`agent.yaml` is an [`LLMAgent`](https://github.com/sandbox-cloud/protos) resource
(snake_case proto fields). The agent **name** is the CLI argument, not a YAML
field. Names are lowercase letters, digits, and dashes, at most 20 characters.

## Package layout

```
agents/<id>/
  manifest.yaml          Required. Hub metadata.
  agent.yaml             Required. Runtime wiring only: brief, details, tools,
                         visibility, sub_agents, model, exec placeholders.
                         Do not put instructions here.
  instructions.md        Required. Persona; compiled into `instructions`.
  skills/<name>/SKILL.md Optional. Agent Skills format (agentskills.io).
  tools/<name>/tool.yaml Optional. CLI capability package.
  tools/<name>/*         Wrappers and supporting files.
  README.md              Required. Human catalog page and attribution.
```

`<id>` must be a valid Crafting agent name (same 20-character rule).

## Manifest

Validated by `schema/manifest.schema.json`.

### Identity

| Field | Type | Notes |
| --- | --- | --- |
| `schema_version` | string | Must be `"0.1"` |
| `id` | string | Directory name and Crafting agent name |
| `name` | string | Display name |
| `category` | enum | `product`, `engineering`, `security`, `operations`, `legal`, `design`, `docs` |
| `description` | string | Catalog blurb |

### Sources (authority bar)

`sources` is a non-empty list. Each entry:

| Field | Type | Notes |
| --- | --- | --- |
| `name` | string | Human label |
| `url` | string | Canonical URL |
| `kind` | enum | `official-vendor`, `popular-oss`, `standard` |
| `stars` | integer | Required when `kind` is `popular-oss`; must be ≥ 10000 |
| `used_for` | string[] | `persona`, `skills`, `tools`, `process` |

Do not take definitions from small "awesome" lists. Prefer official vendor docs
and plugins, then highly starred OSS, then published standards.

### Persona and runtime pointers

```yaml
persona:
  instructions: ./instructions.md
runtime:
  agent: ./agent.yaml
```

### Skills

```yaml
skills:
  - path: ./skills/sprint-planning
    requires: [ticket_board]   # optional capability ids
```

Each `path` is a directory containing `SKILL.md` with YAML frontmatter
`name` and `description` per [agentskills.io](https://agentskills.io/specification).
At compile time, skills are planted at `~/.agents/skills/<name>/` in the exec
template. Crafting discovers them from the workspace filesystem.

If any skill is present, the package **must** produce an exec template.

### Capabilities

A capability is an abstract need (`ticket_board`, `web_scanner`) that one or more
**providers** can satisfy. Providers are `mcp` or `cli`. Not every agent offers
a choice; Product Manager does because the ticket-board ecosystem is large.

```yaml
capabilities:
  ticket_board:
    label: Ticket board
    description: Where this agent works with tickets.
    required: true
    operations: [read_tickets, search_tickets, update_tickets]
    providers:
      - id: jira
        kind: mcp
        connection:
          ref: jira          # org named_mcp_servers key
        tool_mapping:
          read_tickets: jira_get_issue
          search_tickets: jira_search
          update_tickets: jira_update_issue
        configuration:
          project:
            label: Project
            type: string
            required: true
      - id: linear
        kind: mcp
        connection:
          ref: linear
        tool_mapping:
          read_tickets: get_issue
          search_tickets: list_issues
          update_tickets: update_issue
        configuration:
          team:
            label: Team
            type: string
            required: true
    verification:
      - connection_authenticated
      - selected_context_accessible
      - required_capabilities_available
```

#### Provider kinds

**`mcp`**

- `connection.ref` is the name in the org's `named_mcp_servers`. Compiled form:
  `mcp_servers.explicit: [{ ref: <name> }]`.
- Do not inline URLs or tokens in hub files. Custom MCP servers are blocked by
  default org policy.
- `tool_mapping` maps abstract `operations` to provider tool names. Listing Jira
  and Linear as alternatives does **not** make their tools interchangeable; each
  mapping must be reviewed against the live MCP server.
- `configuration` is provider-specific context collected at install (project key,
  team id). The runtime `LLMAgent` has no config field; the installer appends a
  `## Working context` block to `instructions`.

**`cli`**

- `tool` is a relative path to a `tools/<name>/` directory with `tool.yaml`.
- The build plants wrappers via `system.files` and runs the install hook as a
  checkout `post-checkout` command, matching the demo-org web scan template.

#### Verification (UI hints, not runtime)

`verification` is a closed enum consumed by the future Add Agent flow. The
compiler and `cs llm agent create` ignore it.

| Value | Meaning |
| --- | --- |
| `connection_authenticated` | Selected MCP connection answers with stored credentials |
| `selected_context_accessible` | Configuration value (project, team) is readable |
| `required_capabilities_available` | Mapped tools exist on the connected server |
| `cli_executable` | Wrapper exists and the binary is on PATH or at the planted path |

### Collaboration

```yaml
collaboration:
  default_pattern: single_agent
  optional:
    - id: engineering_estimation
      label: Estimate with Engineering Manager
      pattern: delegate_to_agent
      agent_dependency:
        role: engineering-manager
        selection: existing_agent
      requires: [ticket_board]
```

`default_pattern` is `single_agent` unless the agent is a coordinator whose
`agent.yaml` already lists `sub_agents`. Optional patterns are skippable in the
UI. Bundled subagent YAML, installing a dependent hub entry, and dynamic
subagent creation are separate runtime decisions; this field only declares
intent.

Coordinators that always need named specialists (legal-counsel →
contract-analyst) list them in `runtime` `sub_agents` so `cs llm agent create`
wires them the same way agent-patterns does today.

### Use cases

Suggested tasks shown after onboarding and on the agent afterward.

```yaml
use_cases:
  - id: plan_sprint
    label: Plan next sprint
    requires: [ticket_board]
    requires_patterns: []          # optional collaboration ids
    inputs:
      - id: sprint_goal
        label: What should this sprint accomplish?
        type: text
        required: true
    prompt: |
      Review the configured ticket board and propose a sprint plan
      for this goal: {{inputs.sprint_goal}}.
```

Tasks that need an unconfigured optional integration must say so in `label` or
`prompt`.

## Runtime `agent.yaml` (package source)

Only wiring. Allowed fields (LLMAgent proto):

- `brief`, `details`
- `tools.system`, `tools.transfer_to_workspace`
- `visibility.disabled`, `visibility.scope` (`NORMAL` or `SUB_AGENT`)
- `sub_agents[].custom.name` or `sub_agents[].template.{name,agent}`
- `model`, `model_mapping`
- `mcp_servers` — usually omitted in source; filled by the compiler from the
  selected MCP providers
- `exec.use_template.name` — usually omitted in source; the compiler sets
  `hub-<id>` when it emits a template

No `instructions` in this file.

## CLI `tool.yaml`

Validated by `schema/tool.schema.json`.

```yaml
id: lonkero
label: Lonkero web scanner
description: HTTP vulnerability scanner used by the security-scanner agent.
install:
  checkout_path: scan
  cmd: |
    [[ -x ./lonkero ]] || {
      curl -sSfL https://github.com/bountyyfi/lonkero/releases/download/v3.7.3/lonkero-linux-x64.tar.gz | tar -zx
    }
wrappers:
  - dest: ~/scan/scan.sh
    mode: "0755"
    source: ./scan.sh
  - dest: ~/scan/AGENTS.md
    mode: "0644"
    content: |
      Use `./scan.sh URL` to scan the specified URL.
```

`source` is relative to the tool directory. `content` is inline. Exactly one of
`source` or `content` per wrapper.

## Compilation

`python3 scripts/build.py <id> [--provider <capability>=<provider_id> ...]`

1. Load and schema-validate `manifest.yaml`.
2. Load `instructions.md` and source `agent.yaml`.
3. For each `--provider`, require that `id` exists under that capability.
   Required capabilities with no flag and exactly one provider are selected
   automatically. Required capabilities with multiple providers and no flag
   stay unbound (MCP not attached; instructions still refer to "the configured
   ticket board").
4. Set `instructions` to the persona plus, when configuration values are
   supplied later by the UI, a `## Working context` section. The CLI build
   records selected provider ids in that section so the agent knows which board
   it has.
5. For each selected `mcp` provider, append `{ ref: connection.ref }` to
   `mcp_servers.explicit`.
6. If the package has skills or any selected/available `cli` provider, emit
   `dist/<id>/template.yaml`:
   - one workspace (name from the first CLI `checkout_path`, or `agent`)
   - `system.files` for each `SKILL.md` at `~/.agents/skills/<name>/SKILL.md`
   - `system.files` for each wrapper
   - a checkout with `post-checkout` install `cmd` when `install.cmd` is set
   - set `exec.use_template.name` to `hub-<id>`
7. Write `dist/<id>/agent.yaml`.
8. Refresh `catalog.yaml` from all `agents/*/manifest.yaml`.

Pure-MCP agents with **no** skills stay stateless: no template, no `exec`.
Coordinators that declare `sub_agents` should stay stateless for the same
reason: template-exec custom agents do not currently carry the sub-agent
toolset. Put skills on the specialists, not on the manager.

## Catalog protocol

`catalog.yaml` (schema: `schema/catalog.schema.json`):

```yaml
schema_version: "0.1"
hub:
  id: crafting-demo
  name: Crafting Agent Hub
agents:
  - id: product-manager
    name: Product Manager
    category: product
    path: agents/product-manager
    description: >
      Help plan sprints, organize the backlog, and write specs.
```

Crafting lists `agents`, then GET `path/manifest.yaml` and the files it
references. Version selection and update behavior are not specified in `0.1`.

## Validation

`scripts/validate.sh`:

1. Every `agents/*/manifest.yaml` against `schema/manifest.schema.json`
2. Every `tools/*/tool.yaml` against `schema/tool.schema.json`
3. `catalog.yaml` against `schema/catalog.schema.json`
4. Compiled `dist/*/agent.yaml` against `schema/agent.schema.json`
5. Compiled `dist/*/template.yaml` with `cs template validate` when `cs` is
   authenticated; otherwise skip with a warning

There is no `cs llm agent validate`. Agent YAML is checked offline against the
LLMAgent JSON Schema and end-to-end by `cs llm agent create`.

## Out of scope for 0.1

- Hub versioning and rolling catalog updates
- Curation / review process for third-party submissions
- Sandbox packaging beyond the generated exec template
- Inline custom MCP servers
- CoworkerBot as an auth dependency
