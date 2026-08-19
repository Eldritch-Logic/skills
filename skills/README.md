# Skills

One directory per skill, each containing a `SKILL.md`:

```
skills/
  condition-based-waiting/
    SKILL.md        # required
    example.ts      # optional: reusable tool or heavy reference
```

Rules enforced by `scripts/validate.py`:

- Directory name is lowercase-kebab-case and matches the `name` in frontmatter.
- Frontmatter has `name` and `description`, and is under 1024 characters total.
- `description` starts with "Use when …" and states *triggering conditions only* —
  never a summary of the skill's workflow. A description that summarizes the
  workflow becomes a shortcut agents take instead of reading the skill.

Start a new skill with `./scripts/new.sh skill <name>`, and read
`docs/authoring-skills.md` first — skills here are written test-first.
