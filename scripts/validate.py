#!/usr/bin/env python3
"""Validate the structure of this skills repository.

Checks skills, agents, commands, workflows and the plugin/marketplace manifests.
No third-party dependencies: frontmatter is parsed with a deliberately small
scalar-only parser, which is all the formats here need.

Exit status: 0 if there are no errors, 1 otherwise. Warnings never fail the run
unless --strict is passed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_MAX = 1024
DESCRIPTION_SOFT_MAX = 500

errors: list[str] = []
warnings: list[str] = []


def error(path: Path, msg: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def warn(path: Path, msg: str) -> None:
    warnings.append(f"{path.relative_to(ROOT)}: {msg}")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str] | None:
    """Return (fields, raw_frontmatter) or None when the block is missing."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    raw = text[4:end]

    fields: dict[str, str] = {}
    key: str | None = None
    for line in raw.split("\n"):
        if not line.strip():
            continue
        if line[0] in " \t" and key:  # continuation of a folded scalar
            fields[key] += " " + line.strip()
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        fields[key] = value.strip().strip("'\"")
    return fields, raw


def check_markdown(path: Path, required: list[str], kind: str) -> dict[str, str]:
    parsed = parse_frontmatter(path)
    if parsed is None:
        error(path, f"{kind} is missing a YAML frontmatter block (--- ... ---)")
        return {}
    fields, raw = parsed

    if len(raw) > FRONTMATTER_MAX:
        error(path, f"frontmatter is {len(raw)} chars, max is {FRONTMATTER_MAX}")

    for field in required:
        if not fields.get(field):
            error(path, f"frontmatter is missing required field '{field}'")

    description = fields.get("description", "")
    if description:
        if len(description) > DESCRIPTION_SOFT_MAX:
            warn(path, f"description is {len(description)} chars; aim for under {DESCRIPTION_SOFT_MAX}")
        if re.match(r"^\s*(I |I'|We |We')", description):
            warn(path, "description should be third person, not first person")
    return fields


def check_skills() -> None:
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        return
    for entry in sorted(skills_dir.iterdir()):
        if entry.name.startswith(".") or entry.name == "README.md":
            continue
        if entry.is_file():
            warn(entry, "loose file in skills/; each skill belongs in its own directory")
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.is_file():
            error(entry, "skill directory has no SKILL.md")
            continue
        if not SLUG.match(entry.name):
            error(entry, "skill directory name must be lowercase-kebab-case")

        fields = check_markdown(skill_md, ["name", "description"], "skill")
        name = fields.get("name", "")
        if name and not SLUG.match(name):
            error(skill_md, f"name '{name}' must be lowercase-kebab-case (letters, numbers, hyphens)")
        if name and name != entry.name:
            error(skill_md, f"name '{name}' does not match directory name '{entry.name}'")
        description = fields.get("description", "")
        if description and not description.lower().startswith("use when"):
            warn(skill_md, "description should start with 'Use when ...' so triggers are explicit")


def check_flat_markdown(subdir: str, required: list[str], kind: str) -> None:
    directory = ROOT / subdir
    if not directory.is_dir():
        return
    for path in sorted(directory.rglob("*.md")):
        if path.name == "README.md":
            continue
        fields = check_markdown(path, required, kind)
        name = fields.get("name")
        if name and not SLUG.match(name):
            error(path, f"name '{name}' must be lowercase-kebab-case")
        if kind == "agent" and name and name != path.stem:
            error(path, f"name '{name}' does not match filename '{path.stem}'")


def check_workflows() -> None:
    directory = ROOT / "workflows"
    if not directory.is_dir():
        return
    for path in sorted(directory.glob("*.js")):
        text = path.read_text(encoding="utf-8")
        if "export const meta" not in text:
            error(path, "workflow script must begin with 'export const meta = {...}'")
        for banned in ("Date.now(", "Math.random("):
            if banned in text:
                error(path, f"workflow scripts cannot call {banned}) — it breaks resume")


def check_manifests() -> None:
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"

    plugin = None
    for path in (plugin_path, marketplace_path):
        if not path.is_file():
            error(path, "manifest is missing")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            error(path, f"invalid JSON: {exc}")
            continue
        if path is plugin_path:
            plugin = data

    if plugin is None or not marketplace_path.is_file():
        return
    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return

    listed = {entry.get("name"): entry for entry in marketplace.get("plugins", [])}
    entry = listed.get(plugin.get("name"))
    if entry is None:
        error(marketplace_path, f"plugin '{plugin.get('name')}' is not listed in the marketplace")
    elif entry.get("version") != plugin.get("version"):
        error(
            marketplace_path,
            f"version {entry.get('version')} disagrees with plugin.json version {plugin.get('version')}",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()

    check_manifests()
    check_skills()
    check_flat_markdown("agents", ["name", "description"], "agent")
    check_flat_markdown("commands", ["description"], "command")
    check_workflows()

    for message in warnings:
        print(f"warning: {message}")
    sys.stdout.flush()
    for message in errors:
        print(f"error: {message}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    if warnings and args.strict:
        print(f"\n{len(warnings)} warning(s) with --strict", file=sys.stderr)
        return 1
    print(f"OK — 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
