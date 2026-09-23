---
name: implement-change
description: Implement a specified change in a Crafting sandbox using cs to join or create it, then hand off to the workspace agent. Use when you are the implementer, not the reviewer.
---

# Implement a change

1. Resolve sandbox: named sandbox, else named template, else the repo URL
   (one matching template → use it; several → ask; none → create from the
   URL), else new-from-scratch → empty sandbox, else ask for the prior work.
2. Target the workspace. Restate constraints in the transfer (the workspace
   agent drops these instructions).
3. Follow in-repo `AGENTS.md` / `CLAUDE.md` if present.
4. Start template daemons with `cs up` when the change needs running services.
   Do not start services with language toolchains (`go run`, `npm start`).
5. Restart any daemon running the code you changed (`cs restart NAME`), then
   `cs ps`, so the running service reflects the change for whoever verifies it.
6. Report sandbox, workspace, files, endpoints. No PR unless asked.
