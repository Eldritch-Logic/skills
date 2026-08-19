# Contributing

## Adding a skill

Skills are written test-first. Read
[`docs/authoring-skills.md`](docs/authoring-skills.md) before writing one — the
whole process is in there. In brief:

1. **RED** — run the scenario with a subagent, *without* the skill. Record what
   it did wrong, verbatim. If it doesn't fail, there's no skill to write.
2. **GREEN** — scaffold with `./scripts/new.sh skill <name>` and write only the
   guidance that closes those observed failures.
3. **REFACTOR** — re-run the scenario with the skill loaded. Close each new
   loophole the agent finds. Repeat until it holds under pressure.

Include the baseline in your pull request description. A skill without one will
be sent back — not as a formality, but because untested guidance reliably teaches
the wrong thing.

## Adding an agent, command, or workflow

Scaffold with `./scripts/new.sh {agent|command|workflow} <name>`, then:

- **Agents** — the filename must match the `name` in frontmatter. State what the
  agent does *not* handle. Its final message is a return value to a calling
  agent, not a message to a human; say so in the prompt.
- **Commands** — `description` is what users see in the menu. Scope
  `allowed-tools` to what the command actually needs.
- **Workflows** — start with `export const meta = {...}` as a pure literal.
  `Date.now()`, `Math.random()`, and argless `new Date()` are unavailable; they
  break resume. Default to `pipeline()` over `parallel()` unless a stage
  genuinely needs every prior result at once.

Nothing goes in `commands/` that only matters to this repo — those belong in
`.claude/commands/`.

## Before opening a pull request

```bash
python3 scripts/validate.py --strict
```

Must be clean. If you believe a validator rule is wrong, change the rule in the
same PR and say why — don't work around it in the content.

## Versioning

Bump `version` in **both** `.claude-plugin/plugin.json` and the matching entry in
`.claude-plugin/marketplace.json`. The validator fails if they disagree.

## Style

- Filenames and skill names: lowercase-kebab-case, verb-first where natural
  (`condition-based-waiting`, not `async-test-helpers`).
- Descriptions: third person, start with "Use when", triggering conditions only —
  never a summary of the workflow.
- One excellent example beats the same pattern in five languages.
