#!/usr/bin/env python3
"""Validate hub manifests and compiled artifacts without extra packages.

Uses jsonschema when it is importable; otherwise a required-field / enum /
pattern checker that covers schema/v0.1.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def load_yaml(path: Path) -> Any:
    with path.open() as f:
        return yaml.safe_load(f)


def fail(path: Path, loc: str, msg: str, errors: list[str]) -> None:
    errors.append(f"{path} {loc}: {msg}")


def check_type(value: Any, expected: str) -> bool:
    mapping = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "boolean": bool,
    }
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    cls = mapping.get(expected)
    return cls is not None and isinstance(value, cls)


def fallback_validate(instance: Any, schema: dict, path: Path) -> list[str]:
    errors: list[str] = []

    def walk(node: Any, sch: dict, loc: str) -> None:
        if "$ref" in sch:
            ref = sch["$ref"]
            if ref.startswith("#/$defs/"):
                name = ref.split("/")[-1]
                defs = schema.get("$defs") or {}
                if name not in defs:
                    fail(path, loc, f"unknown $ref {ref}", errors)
                    return
                merged = {k: v for k, v in sch.items() if k != "$ref"}
                walk(node, {**defs[name], **merged}, loc)
                return
        if "const" in sch and node != sch["const"]:
            fail(path, loc, f"expected {sch['const']!r}", errors)
        if "enum" in sch and node not in sch["enum"]:
            fail(path, loc, f"expected one of {sch['enum']}", errors)
        types = sch.get("type")
        if types:
            allowed = types if isinstance(types, list) else [types]
            if not any(check_type(node, t) for t in allowed):
                fail(path, loc, f"type {type(node).__name__} not in {allowed}", errors)
                return
        if "pattern" in sch and isinstance(node, str):
            if not re.search(sch["pattern"], node):
                fail(path, loc, f"does not match {sch['pattern']}", errors)
        if "maxLength" in sch and isinstance(node, str) and len(node) > sch["maxLength"]:
            fail(path, loc, f"longer than {sch['maxLength']}", errors)
        if "minLength" in sch and isinstance(node, str) and len(node) < sch["minLength"]:
            fail(path, loc, f"shorter than {sch['minLength']}", errors)
        if "minItems" in sch and isinstance(node, list) and len(node) < sch["minItems"]:
            fail(path, loc, f"fewer than {sch['minItems']} items", errors)
        if "minimum" in sch and isinstance(node, int) and node < sch["minimum"]:
            fail(path, loc, f"below minimum {sch['minimum']}", errors)
        if sch.get("type") == "object" and isinstance(node, dict):
            required = sch.get("required") or []
            for key in required:
                if key not in node:
                    fail(path, loc, f"missing required {key!r}", errors)
            props = sch.get("properties") or {}
            addl = sch.get("additionalProperties", True)
            for key, val in node.items():
                if key in props:
                    walk(val, props[key], f"{loc}.{key}" if loc != "<root>" else key)
                elif addl is False:
                    fail(path, loc, f"unexpected property {key!r}", errors)
                elif isinstance(addl, dict):
                    walk(val, addl, f"{loc}.{key}" if loc != "<root>" else key)
        if sch.get("type") == "array" and isinstance(node, list) and "items" in sch:
            item_sch = sch["items"]
            for i, item in enumerate(node):
                walk(item, item_sch, f"{loc}[{i}]")
        for clause in sch.get("allOf") or []:
            walk(node, clause, loc)
        if_sch = sch.get("if")
        if if_sch and isinstance(node, dict):
            pred = True
            for k, v in (if_sch.get("properties") or {}).items():
                if "const" in v and node.get(k) != v["const"]:
                    pred = False
            for k in if_sch.get("required") or []:
                if k not in node:
                    pred = False
            branch = sch.get("then") if pred else sch.get("else")
            if branch:
                walk(node, branch, loc)

    walk(instance, schema, "<root>")
    return errors


def jsonschema_validate(instance: Any, schema: dict, path: Path) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
        from jsonschema import validators
    except ImportError:
        return fallback_validate(instance, schema, path)

    try:
        validator = Draft202012Validator(schema)
    except Exception:
        cls = validators.validator_for(schema)
        validator = cls(schema)
    errors = []
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "<root>"
        errors.append(f"{path} {loc}: {err.message}")
    return errors


def check(instance: Any, schema: dict, path: Path) -> bool:
    errors = jsonschema_validate(instance, schema, path)
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f"  {e}")
        return True
    print(f"ok   {path}")
    return False


def extra_authority_rules(manifest: dict, path: Path) -> bool:
    failed = False
    for i, src in enumerate(manifest.get("sources") or []):
        if src.get("kind") == "popular-oss":
            stars = src.get("stars")
            if not isinstance(stars, int) or stars < 10000:
                print(f"FAIL {path} sources[{i}].stars: popular-oss requires stars >= 10000")
                failed = True
    ident = manifest.get("id", "")
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,18}[a-z0-9]", ident) or len(ident) > 20:
        print(f"FAIL {path} id: must be a Crafting agent name (<=20, [a-z0-9-])")
        failed = True
    if manifest.get("id") != path.parent.name:
        print(f"FAIL {path} id {manifest.get('id')!r} != directory {path.parent.name!r}")
        failed = True
    return failed


def main() -> int:
    schema_dir = ROOT / "schema"
    manifest_schema = load_json(schema_dir / "manifest.schema.json")
    tool_schema = load_json(schema_dir / "tool.schema.json")
    catalog_schema = load_json(schema_dir / "catalog.schema.json")
    agent_schema = load_json(schema_dir / "agent.schema.json")

    failed = False
    for manifest_path in sorted((ROOT / "agents").glob("*/manifest.yaml")):
        data = load_yaml(manifest_path)
        failed = check(data, manifest_schema, manifest_path) or failed
        failed = extra_authority_rules(data, manifest_path) or failed
        pkg = manifest_path.parent
        for tool_yaml in sorted(pkg.glob("tools/*/tool.yaml")):
            failed = check(load_yaml(tool_yaml), tool_schema, tool_yaml) or failed

    failed = check(load_yaml(ROOT / "catalog.yaml"), catalog_schema, ROOT / "catalog.yaml") or failed

    for compiled in sorted((ROOT / "dist").glob("*/agent.yaml")):
        failed = check(load_yaml(compiled), agent_schema, compiled) or failed

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
