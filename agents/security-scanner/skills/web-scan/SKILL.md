---
name: web-scan
description: Run the planted scan.sh CLI against a URL, parse JSON findings, and report them by severity. Use when asked to scan, re-scan, or verify that a vulnerability was fixed. Never write exploits.
---

# Web scan

## Command

```
/home/owner/scan/scan.sh [flags] URL
```

`scan.sh` is planted by the hub exec template. It requests a sandbox endpoint
cookie and execs lonkero.

## Steps

1. Confirm the URL (and any mode flags) from the request.
2. Run the command. Capture the full JSON.
3. Summarize findings. Map to OWASP Top 10 / CWE labels when the mapping is
   obvious; otherwise describe the observation without stretching.
4. On re-scan, diff against the previous finding list in this conversation.

## Do not

- Write or suggest exploit payloads
- Change application code
- Skip the CLI and guess from the URL string
