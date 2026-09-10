# Integration Tester

Cluster verification specialist. Runs after `qa-engineer` passes locally,
when the template defines a Kubernetes intercept plan. Reports skipped
rather than guessing when no plan exists.

`engineering-manager` lists this agent as an optional `cluster_verification`
collaboration. It is not one of that agent's wired sub-agents, so install it
only when your templates have intercept plans.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [Crafting Kubernetes intercept plan](https://docs.sandboxes.cloud/guides/developers/kubernetes-intercept-plan.html) | official-vendor | `cs k8s intercept start --plan`, plan defined in the template |
| [Crafting Kubernetes development experience](https://docs.sandboxes.cloud/features/kubernetes-dev-experience.html) | official-vendor | Traffic interception and rerouting model |
| [Anthropic best practices](https://code.claude.com/docs/en/best-practices) | official-vendor | Verification in a fresh session that did not write the change |
