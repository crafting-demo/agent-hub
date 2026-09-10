---
name: diagnose-incident
description: Reproduce a symptom in a sandbox and optionally compare via Kubernetes intercept. Report diagnosis. Do not patch.
---

# Diagnose an incident

1. Restate the symptom. Name the template.
2. Reproduce locally (`cs up` / `cs ps`, named flow, evidence).
3. Intercept only if a plan exists.
4. Write diagnosis: reproduced?, where?, ruled out, sandbox, next step.
5. No product edits. No implementer spawn.
