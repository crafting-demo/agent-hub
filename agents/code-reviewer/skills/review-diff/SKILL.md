---
name: review-diff
description: Read-only review of a git diff for quality, correctness, and defensive security - secrets, injection, authn/authz, insecure defaults - mapped to OWASP Top 10 and CWE. Use when a change already exists and you must not patch it. Never write exploits.
---

# Review a diff

1. Join the named sandbox. Do not create one.
2. Obtain the diff (default branch, else HEAD, else working tree).
3. Load project norms if present.
4. Review quality and correctness.
5. Review security: secrets, injection on untrusted input, authn/authz on
   changed endpoints, insecure defaults, and dependency or config changes
   that widen the attack surface. Map to OWASP Top 10 / CWE only where the
   mapping is obvious.
6. Publish one Critical / Suggestions / Good practices review with file refs.
   Security findings carry severity, risk, and a remediation hint.
7. Found nothing under a lens? Say so explicitly and name what you examined.

## Do not

- Write exploits, payloads, or proof of concept attacks
- Edit, commit, push, or patch
- Claim the change is fine without saying what you checked
