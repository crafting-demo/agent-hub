# Crafting Agent Hub

Curated, purpose-built agents for Crafting. Each package is a persona, a set of
skills, and abstract capabilities that resolve to a CLI or an MCP provider at
install time. One Product Manager works with Jira or Linear; you do not need a
separate agent per ticket board.

This repository is the programmatic source for the Agents Hub catalog. Multi-agent
demos live in [crafting-demo/agent-patterns](https://github.com/crafting-demo/agent-patterns)
and install agents from here. Hub-backed patterns: vendor contract review,
secure delivery, backlog to reviewed change.

## Layout

```
catalog.yaml                 Hub index (HTTP entrypoint)
SPEC.md                      Package format contract
schema/                      JSON Schema for manifests, tools, catalog, compiled agents
scripts/build.py             Compile a package into LLMAgent YAML (+ sandbox template)
scripts/validate.sh          Schema checks; `cs template validate` when logged in
agents/<id>/
  manifest.yaml              Identity, sources, capabilities, use cases
  agent.yaml                 Runtime wiring only (no instructions)
  instructions.md            Persona (source of truth)
  skills/<skill>/SKILL.md    Agent Skills (agentskills.io)
  tools/<tool>/              CLI installers and wrappers
  README.md                  Catalog page and attribution
```

## Install an agent

Requires the [Crafting `cs` CLI](https://docs.sandboxes.cloud).

```sh
python3 scripts/build.py product-manager --provider ticket_board=jira
cs llm agent create product-manager --shared dist/product-manager/agent.yaml
```

If the package ships skills or a CLI, also create the generated template first:

```sh
python3 scripts/build.py security-scanner
cs template create hub-security-scanner dist/security-scanner/template.yaml   # or: cs template update
cs template validate dist/security-scanner/template.yaml
cs llm agent create security-scanner --shared dist/security-scanner/agent.yaml
```

Omit `--shared` if you are not an org admin. If the name already exists, use
`cs llm agent update` instead of `create`.

MCP providers bind to org `named_mcp_servers` by `ref`. The compiled agent never
embeds credentials.

## Catalog protocol

Crafting discovers entries from `catalog.yaml` at the repository root, then
fetches each `path` and reads `manifest.yaml`. Raw GitHub URLs are enough for
the first hub:

- `https://raw.githubusercontent.com/crafting-demo/agent-hub/main/catalog.yaml`
- `https://raw.githubusercontent.com/crafting-demo/agent-hub/main/agents/<id>/manifest.yaml`

Customers can host another hub with the same layout.

## Authority

Every agent lists `sources` in its manifest. Allowed kinds:

- `official-vendor` — Anthropic, OpenAI, Google, GitHub, OWASP, and similar
- `popular-oss` — GitHub repositories with at least 10,000 stars
- `standard` — published specifications (Agent Skills, OWASP Top 10, CWE)

We paraphrase published process. We do not vendor other vendors' plugin files.

## License

Apache-2.0 for original Crafting YAML, instructions, and skills in this
repository. Upstream sources remain under their own licenses; see each agent's
`README.md`.
