---
name: security-review
description: Read-only defensive security review of a diff - secrets, injection, authn/authz, insecure defaults - mapped to OWASP Top 10 and CWE. Use when a change exists and needs a security gate. Never write exploits.
---

# Security review

1. Join the named sandbox. Do not create one.
2. Get the diff: `git diff` against the default branch, else `git diff
   HEAD`, else review the working tree.
3. Check secrets, injection on untrusted input, authn/authz on changed
   endpoints, insecure defaults, and dependency or config changes that
   widen the attack surface.
4. Map to OWASP Top 10 / CWE only where the mapping is obvious.
5. Report Critical / Suggestions / Good practices with file references,
   each with severity, location, risk, and a remediation hint.
6. No findings? Say so explicitly and name what you examined.

## Do not

- Write exploits, payloads, or proof of concept attacks
- Edit, commit, push, or patch
- Claim the change is fine without saying what you checked
