# QA Engineer

Verification specialist. Pairs with `engineering-manager` and
`software-engineer`.

Local and cluster verification are the same job against two environments, so
they are one agent with two skills, not two agents. Each request is a single
pass: `engineering-manager` asks for the local pass, then sends a second,
separate request for the cluster pass. That keeps the cluster result from
being graded by the session that just passed locally.

The cluster pass needs a Kubernetes
[intercept plan](https://docs.sandboxes.cloud/guides/developers/kubernetes-intercept-plan.html)
in the template. With no plan the agent reports skipped rather than guessing.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [Anthropic best practices](https://code.claude.com/docs/en/best-practices) | official-vendor | Fresh-session verification |
| [microsoft/playwright](https://github.com/microsoft/playwright) (96k stars) | popular-oss | Web UI flow checks |
| [Crafting Kubernetes intercept plan](https://docs.sandboxes.cloud/guides/developers/kubernetes-intercept-plan.html) | official-vendor | `cs k8s intercept start --plan`, plan defined in the template |
| [Crafting Kubernetes development experience](https://docs.sandboxes.cloud/features/kubernetes-dev-experience.html) | official-vendor | Traffic interception and rerouting model |
