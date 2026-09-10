# Sources

Hub personas and skills follow **published** agent designs. Crafting YAML
(sandbox join, `cs`, org-shared agents, capability manifests) is ours. We
paraphrase process. We do not vendor other vendors' plugin files.

Authority bar: official vendor, published standard, or GitHub ≥ 10,000 stars.

| Agent | Primary sources |
| --- | --- |
| pde-lead | [Get Shit Done](https://github.com/gsd-build/get-shit-done) discuss-phase (64.5k, archived); [Anthropic subagents](https://code.claude.com/docs/en/sub-agents) |
| product-manager | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) product-management (23.9k); Get Shit Done locked decisions and deferred ideas; [Agent Skills](https://agentskills.io/specification) |
| design-lead | [Anthropic frontend-design plugin](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) (144.6k); [OpenAI frontend-skill](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4) and [openai/skills](https://github.com/openai/skills) (26.8k) |
| engineering-manager | [google/adk-python](https://github.com/google/adk-python) SequentialAgent (21k); [Anthropic subagents](https://code.claude.com/docs/en/sub-agents); Get Shit Done planner and roadmapper; [Anthropic best practices](https://code.claude.com/docs/en/best-practices) (plan before code) |
| software-engineer | [Anthropic best practices](https://code.claude.com/docs/en/best-practices); [OpenAI AGENTS.md](https://developers.openai.com/codex/guides/agents-md) |
| qa-engineer | Anthropic fresh-session verification; [microsoft/playwright](https://github.com/microsoft/playwright) (96k); [Crafting Kubernetes intercept plan](https://docs.sandboxes.cloud/guides/developers/kubernetes-intercept-plan.html) and [Kubernetes dev experience](https://docs.sandboxes.cloud/features/kubernetes-dev-experience.html) for the cluster pass |
| code-reviewer | [anthropics/claude-code](https://github.com/anthropics/claude-code) (145k) pr-review-toolkit; [GitHub Copilot review-code](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/review-code); [Anthropic subagents](https://code.claude.com/docs/en/sub-agents) read-only security-reviewer contract; OWASP Top 10; [CWE](https://cwe.mitre.org/) |
| security-scanner | Crafting webscan CLI-in-template; OWASP Top 10 |
| incident-commander | Anthropic reviewer contract (report, do not edit); Google ADK sequential |
| legal-counsel | [knowledge-work-plugins legal](https://github.com/anthropics/knowledge-work-plugins/tree/main/legal); [claude-for-legal](https://github.com/anthropics/claude-for-legal) (draft for attorney review) |
| contract-analyst | same legal plugin, `/review-contract` process; [jgm/pandoc](https://github.com/jgm/pandoc) (46k) as the document-conversion tool |
| compliance-reviewer | same legal plugin, `/compliance-check` process; [jgm/pandoc](https://github.com/jgm/pandoc) (46k) as the document-conversion tool |

Star counts were recorded at authoring time (2026-09-10) and are snapshots.

**Get Shit Done.** The repository we cite, [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) (64.5k), is **archived**. It is the source of record for the definition-phase process because it clears the star bar and its workflows are still public. Active development moved to [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core) (9.3k), which is below the bar today; watch it and re-point these manifests when it clears 10k. GSD is a community methodology, not a vendor publication, and we paraphrase it rather than vendoring its workflow files.
