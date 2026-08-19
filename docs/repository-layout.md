# Repository layout

This repo is simultaneously a **Claude Code plugin** and a **plugin marketplace**
that lists it. The plugin root is the repo root, so the top-level content
directories are the ones Claude Code loads.

| Path | What lives here | Loaded as |
|------|-----------------|-----------|
| `skills/<name>/SKILL.md` | Agent skills | Skills, invoked via the `Skill` tool or by name |
| `agents/<name>.md` | Subagent definitions | `subagent_type` values for the `Agent` tool |
| `commands/<name>.md` | Slash commands | `/<name>` for anyone who installs the plugin |
| `workflows/<name>.js` | Workflow scripts | Passed to the `Workflow` tool via `scriptPath` |
| `templates/` | Starting points for new artifacts | Nothing — inert |
| `scripts/` | Repo tooling (validator, scaffolder) | Nothing — inert |
| `docs/` | Authoring guides | Nothing — inert |
| `.claude-plugin/plugin.json` | Plugin manifest (name, version) | Plugin metadata |
| `.claude-plugin/marketplace.json` | Marketplace listing pointing at `./` | Marketplace metadata |
| `.claude/commands/` | Commands for working **on this repo** | `/new`, `/validate` — local only, not shipped |

## Shipped vs. local

`commands/` ships to everyone who installs the plugin. `.claude/commands/` is
project-local and only exists for people working in this checkout. Repo
maintenance commands belong in `.claude/`; anything users should get belongs in
`commands/`.

## Don't put a README.md in `agents/` or `commands/`

Every `.md` file in those directories is loaded as a definition. A `README.md` in
`commands/` becomes a `/README` slash command; one in `agents/` becomes a broken
agent. Document those directories here instead. `skills/` is safe, because skills
are discovered as `skills/<name>/SKILL.md`.

## Versioning

`.claude-plugin/plugin.json` and the matching entry in
`.claude-plugin/marketplace.json` must carry the same `version`. The validator
fails the build if they drift.
