# Security Scanner

Catalog agent that scans a URL with a **CLI** planted in an exec sandbox.
This is the reference package for `kind: cli` capabilities. It ports the
demo-org `webscan` agent: `cs llm agent create` plus template `webscan`.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| Crafting demo-org `webscan` LLMAgent + template | official-vendor | Persona, `scan.sh` wrapper, lonkero install hook |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | standard | Finding taxonomy |

The scanner binary is [lonkero](https://github.com/bountyyfi/lonkero) v3.7.3,
the same release the demo-org template already pins. It is a tool dependency,
not a persona source.

## Capabilities

| Capability | Required | Providers |
| --- | --- | --- |
| `web_scanner` | yes | CLI `lonkero` (`./tools/lonkero`) |

## Install

```sh
python3 scripts/build.py security-scanner
cs template create hub-security-scanner dist/security-scanner/template.yaml
cs template validate dist/security-scanner/template.yaml
cs llm agent create security-scanner --shared dist/security-scanner/agent.yaml
```

The compiled agent sets `exec.use_template.name: hub-security-scanner`.
