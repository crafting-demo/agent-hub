---
name: scan-repo
description: Given a git repository URL instead of a running application, clone it into this sandbox, start the application locally with whatever backing services it needs, then run web-scan against the local URL. Use when the target is a repo (github.com/..., .git) rather than an http(s) URL of a live app. Never patch the application; only run it.
---

# Scan a repository

The scanner is black-box DAST: it needs an HTTP(S) URL that serves the
application. A repository URL is not that. Do not point the scanner at the
git host, and do not refuse — stand the app up in this sandbox and scan it.

## Steps

1. Clone into the `scan` workspace, outside `~/scan` (for example
   `~/targets/<repo-name>`). Do not create or enter another sandbox.
2. Read the repo's README, `package.json` / `pyproject.toml` / `go.mod` /
   `Dockerfile` / `docker-compose*.yml` to learn the runtime, start command,
   port, and backing services.
3. Start backing services the app requires (databases, caches, queues) as
   local containers or processes. When the code hardcodes a hostname such as
   `mongodb://database:27017`, prefer env vars the app already reads; if
   there is none, add an `/etc/hosts` alias for that hostname. Run any seed
   or migration scripts the README calls for so the app has data to expose.
4. Install dependencies and start the app on a **free** port, bound to all
   interfaces (not only `127.0.0.1`). `3000` belongs to the bundled Juice
   Shop target; pick another (`3100`, `8080`, …). Confirm it answers by
   workspace hostname: `curl -sSf -o /dev/null -w '%{http_code}' http://scan:PORT/`.
5. Follow the Web scan procedure against `http://scan:PORT` (plus any deep
   paths the request names). Use the workspace hostname, not `localhost`:
   the scanner's crawler skips `localhost`, so a localhost scan silently
   covers only the entry page. Every workspace in the sandbox is reachable by
   its name, which is why the bundled target is `http://target:3000`.
6. Report as usual, then add a **Setup** section: repo and commit scanned,
   what you started (ports, containers, hosts aliases, seed scripts), and
   anything you could not bring up. Leave everything running for a re-scan
   unless asked to tear it down, and list it so the user can.

## Rules

- Running the app is in scope. Changing its source to make it start, fixing
  its bugs, or patching findings is not. If it will not start, report why and
  stop.
- Static analysis is not what this tool does. If the request is really about
  dependency CVEs or secrets in the code, say so and suggest `code-reviewer`;
  still run the DAST scan if the app can be started.
- Note scanner coverage honestly: findings inferred from a framework version
  (`verified: false`) are not the same as observed behavior.
