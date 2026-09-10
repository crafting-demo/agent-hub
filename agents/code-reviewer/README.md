# Code Reviewer

Single catalog agent covering the quality, logic, and security lenses that
agent-patterns splits across `cr-quality` / `cr-logic` / `cr-sec`. Output
shape is GitHub Copilot review-code.

Security is a lens here, not a separate agent: same input (a diff), same
read-only contract, same report. Ask for a security-only review with the
`review_diff_security` task and the agent narrows the review to secrets,
injection, authn/authz, insecure defaults, and attack surface widened by
dependency or config changes.

`security-scanner` is the different job — it probes a running URL with a CLI
rather than reading a diff.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) (145k stars) pr-review-toolkit / code-review | popular-oss | Reviewer split, read-only contract |
| [GitHub Copilot review-code](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/review-code) | official-vendor | Critical / Suggestions / Good practices |
| [Anthropic subagents](https://code.claude.com/docs/en/sub-agents) | official-vendor | Read-only security-reviewer contract: report, do not edit |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | standard | Security taxonomy |
| [CWE](https://cwe.mitre.org/) | standard | Weakness identifiers |
| [OpenAI AGENTS.md](https://developers.openai.com/codex/guides/agents-md) | official-vendor | In-repo norms |

Crafting has no tool allowlist on `LLMAgent`; the read-only contract is
enforced in instructions and restated on every workspace transfer.
