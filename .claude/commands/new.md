---
description: Scaffold a new skill, agent, command, or workflow in this repo
argument-hint: skill|agent|command|workflow <kebab-case-name>
allowed-tools: Bash, Read, Edit, Write
---

Scaffold a new artifact in this repository.

Run `./scripts/new.sh $ARGUMENTS`, then open the created file.

If the kind is `skill`, do NOT start writing the skill body yet. Skills in this
repo follow the RED-GREEN-REFACTOR loop in `docs/authoring-skills.md`:

1. **RED** — dispatch a subagent at the task this skill is meant to govern,
   without the skill, and record verbatim what it got wrong.
2. **GREEN** — write only the guidance that closes those specific failures.
3. **REFACTOR** — re-run the scenario, close the new loopholes it finds.

Tell the user which phase you are in and what the baseline showed before you
write any skill body. Finish with `python3 scripts/validate.py`.
