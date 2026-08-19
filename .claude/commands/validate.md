---
description: Validate every skill, agent, command, workflow, and manifest in this repo
allowed-tools: Bash, Read, Edit
---

Run `python3 scripts/validate.py --strict`.

Report the result plainly. If there are errors or warnings, fix each one at its
source file and re-run until the output is clean — do not relax the validator to
make a check pass unless the rule itself is wrong, and say so explicitly if you
conclude that it is.
