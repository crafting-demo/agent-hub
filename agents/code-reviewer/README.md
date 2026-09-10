# Code Reviewer

Single catalog agent covering the quality, logic, and security lenses that
agent-patterns splits across `cr-quality` / `cr-logic` / `cr-sec`. Output
shape is GitHub Copilot review-code.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) (145k stars) pr-review-toolkit / code-review | popular-oss | Reviewer split, read-only contract |
| [GitHub Copilot review-code](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/review-code) | official-vendor | Critical / Suggestions / Good practices |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | standard | Security taxonomy |
| [OpenAI AGENTS.md](https://developers.openai.com/codex/guides/agents-md) | official-vendor | In-repo norms |
