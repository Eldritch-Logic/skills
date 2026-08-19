# Authoring skills

Skills in this repo are written **test-first**. The test is a subagent running a
realistic scenario; the failure you are fixing is what that subagent does wrong
without the skill.

> This process follows the `superpowers:writing-skills` skill. Read it for the
> full treatment — the rationalization tables, pressure-scenario design, and the
> persuasion research behind bulletproofing. What follows is the working loop.

## The iron law

**No skill without a failing baseline first.** This applies to edits, not just
new skills. If you didn't watch an agent fail without the guidance, you don't
know whether the guidance teaches the right thing — and you will write words that
feel right and change nothing.

## RED — get the baseline

Dispatch a subagent at the task the skill is meant to govern, with no skill
loaded. Record **verbatim**:

- What it actually did (not what it said it would do)
- The exact rationalizations it used to justify the wrong move
- Which pressures triggered the failure — time, sunk cost, authority, exhaustion

Keep baselines in `tmp/` (gitignored) or paste them into the PR description.

**If the baseline doesn't fail, stop.** There is no skill to write.

## GREEN — write only what closes the baseline

Write the minimum guidance that addresses the specific failures you observed. No
content for hypothetical cases.

Match the form to the failure — the shape that fixes one kind backfires on
another:

| Baseline failure | Right form |
|------------------|-----------|
| Knows the rule, violates it under pressure | Prohibition + rationalization table + red-flags list |
| Complies, but the output has the wrong shape | Positive recipe: state what the output **is**, its parts, in order |
| Omits a required element | Structural: a REQUIRED slot in the template they already fill in |
| Behavior should depend on a condition | Conditional on an *observable* predicate |

Prohibitions backfire on shaping problems: under a competing incentive, agents
negotiate with "don't X". A recipe leaves nothing to negotiate.

Two rules regardless of form:

- **No nuance clauses.** "Don't X unless it matters" reopens the negotiation.
- **Exemption clauses don't scope.** "This limit doesn't apply to code blocks"
  still suppresses code blocks. Restructure so the rule can't reach the exempt part.

## REFACTOR — close the loopholes

Re-run the same scenario with the skill loaded. When the agent finds a *new*
rationalization, add an explicit counter and run again. Repeat until it holds
under the combined pressures, not just one at a time.

Cheap iteration: micro-test the wording first. One fresh-context sample per rep,
5+ reps per variant, **always with a no-guidance control**, and read every
flagged match by hand — template echoes look like hits. Convergence is the
signal: if five reps produce five different interpretations, the wording isn't
binding yet. Micro-tests check wording; they don't replace the full scenario.

## Writing the description

The `description` field decides whether an agent ever opens your skill, so it is
the highest-leverage line in the file.

```yaml
# Bad — summarizes the workflow; agents follow the summary and skip the file
description: Use when executing plans - dispatches a subagent per task with review between tasks

# Good — triggering conditions only
description: Use when executing implementation plans with independent tasks in the current session
```

Include the words someone would search for: error messages, symptoms
("flaky", "hangs", "race condition"), tool and library names. Write in third
person. Describe the *problem*, not language-specific symptoms, unless the skill
really is technology-specific.

## Keep it short

Token cost is real — skill descriptions load into every conversation, and skill
bodies load whenever they are invoked.

- Frequently-loaded skills: under 200 words
- Everything else: under 500 words

Move flag-by-flag detail into `--help` output. Cross-reference other skills by
name (`**REQUIRED BACKGROUND:** superpowers:test-driven-development`) rather than
restating them, and never with `@` — that force-loads the file.

## Before you open a PR

- [ ] Baseline recorded, showing a real failure
- [ ] Skill addresses those specific failures and nothing hypothetical
- [ ] Guidance form matches the failure type
- [ ] Scenario re-run with the skill; agent complies
- [ ] `description` starts with "Use when" and summarizes no workflow
- [ ] One excellent example, not the same pattern in five languages
- [ ] `python3 scripts/validate.py --strict` is clean
