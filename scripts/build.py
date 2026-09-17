#!/usr/bin/env python3
"""Compile Agent Hub packages into Crafting LLMAgent YAML.

Skills are inlined into the agent's instructions. An exec template is emitted
only when a selected CLI provider needs files or a binary on disk, or the
package ships a sandbox fragment of extra workloads to merge in.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
DIST = ROOT / "dist"
SCHEMA = ROOT / "schema"


class LiteralStr(str):
    """Force YAML literal block style for multiline strings."""


def _literal_representer(dumper: yaml.Dumper, data: LiteralStr):
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.add_representer(LiteralStr, _literal_representer)


def load_yaml(path: Path) -> Any:
    with path.open() as f:
        return yaml.safe_load(f)


def dump_yaml(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=88,
        )


def read_text(path: Path) -> str:
    return path.read_text().rstrip() + "\n"


def parse_skill(skill_dir: Path) -> tuple[str, str, str]:
    """Return (name, description, body) from a SKILL.md with frontmatter."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise SystemExit(f"missing {skill_md}")
    text = skill_md.read_text()
    meta: dict = {}
    body = text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        meta = yaml.safe_load(fm) or {}
    name = str(meta.get("name") or skill_dir.name)
    description = " ".join(str(meta.get("description") or "").split())
    return name, description, body.strip()


def demote_headings(markdown: str, levels: int) -> str:
    """Push Markdown headings down so a skill body nests under its section."""
    out: list[str] = []
    in_fence = False
    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("#"):
            hashes = len(line) - len(line.lstrip("#"))
            if line[hashes : hashes + 1] == " ":
                line = "#" * min(hashes + levels, 6) + line[hashes:]
        out.append(line)
    return "\n".join(out)


def skills_context(package: Path, manifest: dict) -> str:
    """Inline every skill so the agent needs no files on disk to use it.

    Rendered as "Procedures", without the word "skill" and without the skill's
    slug. The sandbox agent runtime registers an `activate_skill` tool that
    resolves names against SKILL.md files on disk. Presenting these inlined
    procedures as skills, each headed by its slug, led agents to call that tool
    and fail with "skill not found" for a procedure they already had in context.
    """
    skills = manifest.get("skills") or []
    if not skills:
        return ""
    lines = [
        "",
        "",
        "## Procedures",
        "",
        "Each procedure below is part of your instructions. When a request",
        "matches a procedure's description, follow its steps.",
    ]
    for skill in skills:
        skill_dir = (package / skill["path"]).resolve()
        name, description, body = parse_skill(skill_dir)
        title = name
        body_lines = body.splitlines()
        if body_lines and body_lines[0].startswith("# "):
            title = body_lines[0][2:].strip()
            body = "\n".join(body_lines[1:]).strip()
        lines += ["", f"### {title}", ""]
        if description:
            lines += [description, ""]
        lines.append(demote_headings(body, 2))
    return "\n".join(lines)


def resolve_package(agent_id: str) -> Path:
    path = AGENTS / agent_id
    if not path.is_dir():
        raise SystemExit(f"unknown agent {agent_id!r} (expected {path})")
    return path


def parse_providers(flags: list[str]) -> dict[str, str]:
    selected: dict[str, str] = {}
    for raw in flags:
        if "=" not in raw:
            raise SystemExit(f"--provider must be capability=provider_id, got {raw!r}")
        cap, pid = raw.split("=", 1)
        selected[cap] = pid
    return selected


def pick_providers(manifest: dict, flags: dict[str, str]) -> dict[str, dict]:
    """Return capability_id -> provider dict for this build."""
    chosen: dict[str, dict] = {}
    caps = manifest.get("capabilities") or {}
    for cap_id, cap in caps.items():
        providers = {p["id"]: p for p in cap.get("providers") or []}
        if cap_id in flags:
            pid = flags[cap_id]
            if pid not in providers:
                raise SystemExit(
                    f"provider {pid!r} not on capability {cap_id!r}; "
                    f"have {sorted(providers)}"
                )
            chosen[cap_id] = providers[pid]
            continue
        if cap.get("required") and len(providers) == 1:
            chosen[cap_id] = next(iter(providers.values()))
    unknown = set(flags) - set(caps)
    if unknown:
        raise SystemExit(f"unknown capability in --provider: {sorted(unknown)}")
    return chosen


def working_context(chosen: dict[str, dict]) -> str:
    if not chosen:
        return ""
    lines = ["", "", "## Working context", ""]
    for cap_id, provider in chosen.items():
        kind = provider["kind"]
        lines.append(f"- Capability `{cap_id}` bound to `{provider['id']}` ({kind}).")
        if kind == "mcp":
            ref = (provider.get("connection") or {}).get("ref")
            lines.append(f"  MCP ref: `{ref}`.")
            mapping = provider.get("tool_mapping") or {}
            if mapping:
                pairs = ", ".join(f"{op} → {tool}" for op, tool in mapping.items())
                lines.append(f"  Tool mapping: {pairs}.")
            cfg = provider.get("configuration") or {}
            if cfg:
                keys = ", ".join(cfg)
                lines.append(
                    f"  Install-time configuration fields: {keys}. "
                    "Use the values supplied at onboarding; do not invent them."
                )
        if kind == "cli":
            lines.append("  Use the planted CLI wrappers in this sandbox.")
    return "\n".join(lines)


def stringify_leaves(obj: Any) -> Any:
    """Promote multiline strings to literal blocks in dumped YAML."""
    if isinstance(obj, str) and "\n" in obj:
        return LiteralStr(obj)
    if isinstance(obj, dict):
        return {k: stringify_leaves(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [stringify_leaves(v) for v in obj]
    return obj


def load_tool(package: Path, tool_rel: str) -> tuple[Path, dict]:
    tool_dir = (package / tool_rel).resolve()
    if not tool_dir.is_dir():
        raise SystemExit(f"tool directory missing: {tool_dir}")
    spec = load_yaml(tool_dir / "tool.yaml")
    return tool_dir, spec


FRAGMENT_KEYS = ("workspaces", "dependencies", "containers", "endpoints", "env")
WORKLOAD_KEYS = ("workspaces", "dependencies", "containers")

# An agent's exec template is its runtime, not a template anyone should start a
# sandbox from. This customization hides it from the tools that match templates
# (list_templates, describe_template, create_sandbox_from_template) while
# exec.use_template still resolves it by name.
EXCLUDE_FROM_TEMPLATE_MATCHING = [
    {
        "property_set": {
            "type": "crafting.dev/sandbox/llm",
            "properties": {"authorizedTemplate": "excluded"},
        }
    }
]


def needs_template(manifest: dict, chosen: dict[str, dict]) -> bool:
    """A template is a last resort: files on disk or extra workloads earn one.

    Skills are inlined into instructions, so they never force a template.
    pick_providers already auto-selects single required providers, so an
    optional CLI only counts when it was chosen explicitly.
    """
    if manifest.get("sandbox"):
        return True
    return any(p.get("kind") == "cli" for p in chosen.values())


def load_fragment(package: Path, manifest: dict) -> dict:
    spec = manifest.get("sandbox")
    if not spec:
        return {}
    path = (package / spec["definition"]).resolve()
    if not path.is_file():
        raise SystemExit(f"sandbox definition missing: {path}")
    fragment = load_yaml(path) or {}
    unknown = sorted(set(fragment) - set(FRAGMENT_KEYS))
    if unknown:
        raise SystemExit(
            f"{path}: unsupported keys {unknown}; allowed {list(FRAGMENT_KEYS)}"
        )
    return fragment


def merge_workspace(base: dict, extra: dict) -> dict:
    """Fold a fragment workspace into the generated one of the same name."""
    merged = dict(base)
    for key, value in extra.items():
        if key == "name":
            continue
        if key == "checkouts" and key in merged:
            merged[key] = merged[key] + value
        elif key == "system" and key in merged:
            system = dict(merged[key])
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, list) and isinstance(system.get(sub_key), list):
                    system[sub_key] = system[sub_key] + sub_value
                else:
                    system[sub_key] = sub_value
            merged[key] = system
        else:
            merged[key] = value
    return merged


def check_workload_names(template: dict, package: Path) -> None:
    """The runtime requires one namespace across workspaces/deps/containers."""
    seen: dict[str, str] = {}
    for kind in WORKLOAD_KEYS:
        for item in template.get(kind) or []:
            name = item.get("name")
            if not name:
                raise SystemExit(f"{package}: {kind} entry without a name")
            if name in seen:
                raise SystemExit(
                    f"{package}: workload name {name!r} used by both "
                    f"{seen[name]} and {kind}; names must be unique"
                )
            seen[name] = kind


def build_template(package: Path, manifest: dict, chosen: dict[str, dict]) -> dict:
    files: list[dict] = []
    checkouts: list[dict] = []

    workspace_name = "agent"
    for provider in chosen.values():
        if provider.get("kind") != "cli":
            continue
        tool_dir, spec = load_tool(package, provider["tool"])
        install = spec.get("install") or {}
        checkout_path = install.get("checkout_path", "tool")
        workspace_name = checkout_path
        if install.get("cmd"):
            checkouts.append(
                {
                    "path": checkout_path,
                    "manifest": {
                        "overlays": [
                            {
                                "inline": {
                                    "hooks": {
                                        "post-checkout": {
                                            "cmd": LiteralStr(install["cmd"])
                                        }
                                    }
                                }
                            }
                        ]
                    },
                }
            )
        for wrapper in spec.get("wrappers") or []:
            dest = wrapper["dest"]
            entry: dict[str, Any] = {"path": dest}
            if wrapper.get("mode"):
                entry["mode"] = str(wrapper["mode"])
            if wrapper.get("source"):
                src = tool_dir / wrapper["source"]
                entry["content"] = LiteralStr(read_text(src))
            else:
                content = wrapper.get("content") or ""
                entry["content"] = LiteralStr(content if content.endswith("\n") else content + "\n")
            files.append(entry)

    workspace: dict[str, Any] = {"name": workspace_name}
    if checkouts:
        workspace["checkouts"] = checkouts
    if files:
        workspace["system"] = {"files": files}

    workspaces = [workspace]
    fragment = load_fragment(package, manifest)
    for extra in fragment.get("workspaces") or []:
        name = extra.get("name")
        if not name:
            raise SystemExit(f"{package}: sandbox workspace without a name")
        match = next((i for i, w in enumerate(workspaces) if w["name"] == name), None)
        if match is None:
            workspaces.append(extra)
        else:
            workspaces[match] = merge_workspace(workspaces[match], extra)

    template: dict[str, Any] = {"workspaces": workspaces}
    for key in FRAGMENT_KEYS:
        if key != "workspaces" and fragment.get(key):
            template[key] = fragment[key]
    template["customizations"] = EXCLUDE_FROM_TEMPLATE_MATCHING
    check_workload_names(template, package)
    return template


def compile_agent(agent_id: str, provider_flags: dict[str, str]) -> Path:
    package = resolve_package(agent_id)
    manifest = load_yaml(package / "manifest.yaml")
    if manifest.get("id") != agent_id:
        raise SystemExit(f"{package}/manifest.yaml id {manifest.get('id')!r} != {agent_id!r}")

    runtime_path = package / manifest["runtime"]["agent"]
    runtime = load_yaml(runtime_path) or {}
    if "instructions" in runtime:
        raise SystemExit(f"{runtime_path} must not contain instructions; use instructions.md")

    instructions = read_text(package / manifest["persona"]["instructions"])
    chosen = pick_providers(manifest, provider_flags)
    instructions = (
        instructions.rstrip()
        + working_context(chosen)
        + skills_context(package, manifest)
    )

    compiled = dict(runtime)
    compiled["instructions"] = LiteralStr(instructions)

    mcp_refs: list[dict] = []
    for provider in chosen.values():
        if provider.get("kind") == "mcp":
            ref = (provider.get("connection") or {}).get("ref")
            if not ref:
                raise SystemExit(f"mcp provider {provider.get('id')} missing connection.ref")
            mcp_refs.append({"ref": ref})
    if mcp_refs:
        compiled["mcp_servers"] = {"explicit": mcp_refs}

    out_dir = DIST / agent_id
    template_path = out_dir / "template.yaml"
    if needs_template(manifest, chosen):
        if runtime.get("sub_agents"):
            raise SystemExit(
                f"{agent_id}: a coordinator with sub_agents cannot carry a "
                "template (cli provider or sandbox fragment); template-exec "
                "agents do not get the sub-agent toolset"
            )
        compiled["exec"] = {"use_template": {"name": f"hub-{agent_id}"}}
        template = build_template(package, manifest, chosen)
        dump_yaml(stringify_leaves(template), template_path)
    elif template_path.exists():
        # A stale template from an earlier build would make INSTALL.md create
        # a sandbox template the agent no longer references.
        template_path.unlink()

    dump_yaml(stringify_leaves(compiled), out_dir / "agent.yaml")
    return out_dir


def write_catalog() -> None:
    entries = []
    for manifest_path in sorted(AGENTS.glob("*/manifest.yaml")):
        m = load_yaml(manifest_path)
        entries.append(
            {
                "id": m["id"],
                "name": m["name"],
                "category": m["category"],
                "path": f"agents/{m['id']}",
                "description": m["description"].strip()
                if isinstance(m.get("description"), str)
                else m.get("description"),
            }
        )
    catalog = {
        "schema_version": "0.1",
        "hub": {
            "id": "crafting-demo",
            "name": "Crafting Agent Hub",
            "description": (
                "Curated Crafting agents. Capabilities resolve to MCP or CLI at install."
            ),
        },
        "agents": entries,
    }
    dump_yaml(stringify_leaves(catalog), ROOT / "catalog.yaml")


def list_agent_ids() -> list[str]:
    return sorted(p.parent.name for p in AGENTS.glob("*/manifest.yaml"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "agent_id",
        nargs="?",
        help="Package id under agents/. Omit with --all.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Compile every package.",
    )
    parser.add_argument(
        "--provider",
        action="append",
        default=[],
        metavar="CAPABILITY=PROVIDER",
        help="Bind a capability to a provider id (repeatable).",
    )
    parser.add_argument(
        "--catalog-only",
        action="store_true",
        help="Rewrite catalog.yaml from manifests and exit.",
    )
    args = parser.parse_args(argv)

    if args.catalog_only:
        write_catalog()
        print(f"wrote {ROOT / 'catalog.yaml'}")
        return 0

    flags = parse_providers(args.provider)
    if args.all:
        ids = list_agent_ids()
        if flags:
            raise SystemExit("--provider cannot be combined with --all")
    elif args.agent_id:
        ids = [args.agent_id]
    else:
        parser.error("agent_id or --all is required")

    for agent_id in ids:
        out = compile_agent(agent_id, flags)
        print(f"compiled {agent_id} -> {out}")
    write_catalog()
    print(f"wrote {ROOT / 'catalog.yaml'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
