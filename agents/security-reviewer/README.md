# Security Reviewer

Read-only security specialist for an existing diff. Pairs with
`code-reviewer` when you want security as its own opinion instead of one
lens inside a merged review.

Three security-adjacent agents, three jobs:

| Agent | Reviews | Output |
| --- | --- | --- |
| `security-reviewer` | A diff, statically | Critical / Suggestions / Good practices |
| `security-scanner` | A running URL, with a CLI | Findings by severity |
| `code-reviewer` | A diff, all three lenses merged | One combined review |

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [Anthropic subagents](https://code.claude.com/docs/en/sub-agents) | official-vendor | Read-only security-reviewer contract: report, do not edit |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) pr-review-toolkit (144k stars) | popular-oss | Specialist review split and finding shape |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | standard | Finding taxonomy |
| [CWE](https://cwe.mitre.org/) | standard | Weakness identifiers |

Crafting has no tool allowlist on `LLMAgent`; the read-only contract is
enforced in instructions and restated on every workspace transfer.
