---
name: cluster-verify
description: Verify a sandbox change against a real cluster using Crafting Kubernetes interception. Use after local QA passes and the template has an intercept plan. Report pass, fail, or skipped. Do not patch.
---

# Cluster verify

1. No intercept plan in the request or template? Report skipped and stop.
   Do not invent one.
2. Join the existing sandbox. `cs ps`; `cs up` for template daemons.
3. `cs k8s intercept start --plan PLAN --ingress-disable-auth`, then
   `cs k8s intercept status`.
4. Drive the same flow local QA drove, entering from the cluster rather than
   local ports: the sandbox ingress endpoint, or an in-cluster Service DNS
   name reachable once the plan bridges the cluster network. Use a helper
   script from the template or repo when one exists.
5. Confirm the intercepted service's log in the workspace shows the request,
   so the evidence distinguishes interception from the deployed workload
   answering.
6. Report pass/fail/skipped, plan and status, endpoint hit, observations
   per asserted step, and concrete failures.

No product edits. No PR. Leave the sandbox running unless asked.
