# EldritchLogic Skills

Agent skills, subagents, slash commands, and workflow scripts for agentic
development — packaged as a Claude Code plugin and the marketplace that lists it.

> **Status: scaffold.** The structure, tooling, and authoring process are in
> place; the content directories are intentionally empty. Skills here are written
> test-first (see [`docs/authoring-skills.md`](docs/authoring-skills.md)), so
> nothing ships until it has a recorded baseline failure behind it.

## Install

```
/plugin marketplace add EldritchLogic/skills
/plugin install eldritchlogic@eldritchlogic
```

Everything under `skills/`, `agents/`, and `commands/` becomes available in your
session. Workflow scripts in `workflows/` are run explicitly by path.

## What's in here

| Path | Contents |
|------|----------|
| `skills/` | Agent skills, one directory per skill with a `SKILL.md` |
| `agents/` | Subagent definitions |
| `commands/` | Slash commands |
| `workflows/` | Workflow scripts for multi-agent orchestration |
| `templates/` | Starting points for each of the above |
| `scripts/` | `new.sh` scaffolder, `validate.py` structure checker |
| `docs/` | Authoring guide and repository layout |

Full breakdown: [`docs/repository-layout.md`](docs/repository-layout.md).

## Add something

```bash
./scripts/new.sh skill    my-skill-name
./scripts/new.sh agent    my-agent
./scripts/new.sh command  my-command
./scripts/new.sh workflow my-workflow
```

Then validate:

```bash
python3 scripts/validate.py --strict
```

The validator checks frontmatter fields and length limits, kebab-case naming,
that skill directory names match their `name` field, that agent filenames match
theirs, that workflow scripts declare `meta` and avoid the non-deterministic
calls that break resume, and that `plugin.json` and `marketplace.json` agree on
the version. CI runs it on every push and pull request.

Working inside this repo, `/new` and `/validate` wrap those two scripts.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). The short version: a skill needs a
recorded baseline of an agent failing *without* it before it gets written.

## License

MIT — see [`LICENSE`](LICENSE).
