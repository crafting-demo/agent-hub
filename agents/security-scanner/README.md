# Security Scanner

Catalog agent that scans a URL with a **CLI** planted in an exec sandbox.
This is the reference package for `kind: cli` capabilities and for the
`sandbox` fragment. It ports the demo-org `webscan` agent: `cs llm agent
create` plus template `webscan`.

## Two workspaces

A scanner with nothing to scan demos badly, so this package ships
[`sandbox.yaml`](sandbox.yaml) and the compiled template has two workspaces:

| Workspace | What runs there |
| --- | --- |
| `scan` | The agent. `lonkero` and the `scan.sh` cookie wrapper, planted by the `web_scanner` CLI capability. |
| `target` | OWASP Juice Shop 20.2.0 on port 3000, from the prebuilt release, plus the Node 22 it pins. |

The agent reaches the app over the sandbox network at `http://target:3000`,
which is the default when a request names no URL. Nothing outside the sandbox
is involved, and that is the point: this is the hub's example of an agent
working against services that live with it.

Juice Shop is also published on the sandbox `target` endpoint for a human
watching the demo. That endpoint keeps Crafting's auth proxy — a deliberately
vulnerable app should not be reachable without an org login — and `scan.sh`
injects the endpoint cookie so the agent can scan through it too.

First boot downloads the Node and Juice Shop tarballs (~200 MB) in a
`post-checkout` hook; both are skipped when already present.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| Crafting demo-org `webscan` LLMAgent + template | official-vendor | Persona, `scan.sh` wrapper, lonkero install hook |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | standard | Finding taxonomy |
| [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) | official-vendor | The bundled scan target |

The scanner binary is [lonkero](https://github.com/bountyyfi/lonkero) v3.7.3,
the same release the demo-org template already pins. It is a tool dependency,
not a persona source.

Upstream's `linux-arm64` build of that release links OpenSSL 1.1, which the
Debian 12+ workspace image no longer ships (the x64 build links OpenSSL 3 and
is fine). On arm64 the install hook vendors `libssl.so.1.1` and
`libcrypto.so.1.1` from the Debian bullseye pool into `~/scan/lib`, and
`scan.sh` puts that directory on `LD_LIBRARY_PATH`. The hook ends with
`lonkero --version`, so a broken plant fails the checkout instead of
surfacing as exit 127 at scan time.

## Scanning a repository

The scanner is black-box DAST and needs a running app. When a request names
a git repository instead of a URL, the `scan-repo` procedure has the agent clone
it into the `scan` workspace, start it (with its databases and so on) on a
port other than 3000, and scan `http://localhost:PORT`. It runs the app; it
does not edit it.

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

The compiled agent sets `exec.use_template.name: hub-security-scanner`. The
template must exist before the agent, and it carries both workspaces.
