---
name: local-qa
description: Verify a change against locally running sandbox services. Use Playwright for web UI flows. Report pass or fail. Do not patch.
---

# Local QA

1. Join the existing sandbox. Do not create a new one.
2. `cs ps`; `cs up` / `cs down` for template daemons only.
3. Drive the user flow. Web UI: Playwright. API: real HTTP against local
   ports or sandbox endpoints.
4. Assert at each visible step.
5. Report pass/fail, commands, observations, concrete failures.

No product edits. No PR.
