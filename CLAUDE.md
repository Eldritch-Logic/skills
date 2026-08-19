# Working in this repository

This repo is a Claude Code plugin **and** the marketplace that lists it. The
plugin root is the repo root, so `skills/`, `agents/`, `commands/`, and
`workflows/` are live content — anything you put there ships to users.

## Before you write a skill

Skills here are written test-first. **Do not write a skill body before running
the baseline.** Dispatch a subagent at the task the skill is meant to govern,
without the skill, and record verbatim what it got wrong. That record is what the
skill is allowed to address.

If the baseline doesn't fail, there is no skill to write — say so and stop.

This applies to edits, not just new skills. "It's just adding a section" is the
rationalization this rule exists to block. Full process:
[`docs/authoring-skills.md`](docs/authoring-skills.md).

## Layout rules

- `commands/` ships to users. Repo maintenance commands go in `.claude/commands/`.
- Never create `README.md` in `agents/` or `commands/` — every `.md` there is
  loaded as a definition. Document those directories in `docs/repository-layout.md`.
- Bump `version` in both `.claude-plugin/plugin.json` and the matching
  `.claude-plugin/marketplace.json` entry, or validation fails.

## Commands

```bash
./scripts/new.sh {skill|agent|command|workflow} <kebab-case-name>
python3 scripts/validate.py --strict
```

`/new` and `/validate` wrap these.

## Verification

`python3 scripts/validate.py --strict` must be clean before you claim work is
done. Run it and read the output — don't assert success from having made the
edit. If a validator rule is wrong, change the rule and say why; don't reshape
content to dodge it.
