---
name: shipping-changes
description: Use when committing, pushing, creating a branch or worktree, syncing with the integration branch, resolving merge conflicts, or opening a PR. Read before the first git write operation, not after a hook rejects.
---

# Shipping changes

## Load the project config first

Read `.claude/shipping-changes.md` from the project root before any git write.
It records this project's branch roles, verification gates, hook status, and the
generated artifacts that need regenerating before a PR.

**If that file doesn't exist, initialize before doing anything else** — see
[references/initialization.md](references/initialization.md). It infers the
branch model and the gates from the repository and confirms them with the user.
Working from assumed branch names is how a change lands on a protected branch.

This skill names branches by **role**. Resolve each one in the config:

| Role | What it is |
| ---- | ---------- |
| `mainline` | The production branch. PR-only. |
| `integration` | The branch that deploys to dev/staging, and the sync source. PR-only. |
| `base` | What new work branches from — often `integration`, sometimes a long-lived developer branch. |
| `work` | The short-lived branch you actually commit to. |

Where the config records `integration` as `none`, the project runs a single
protected branch: `integration` collapses onto `mainline` and every rule below
that names `integration` applies to `mainline` instead.

## Branch targets — check before you commit

```
work branch  →  PR into integration  →  PR into mainline
```

**Never push to `mainline` or `integration`.** They advance exclusively through
merged PRs. A direct push skips review _and_ skips the CI run on the branch that
deploys, and there is no way to un-deploy it afterward. If you're already on a
protected branch, branch first, then push the branch.

**Never base a branch or worktree on a protected branch when the config names a
separate `base`.** New work branches off `base`. Where `base` is not the
repository's default branch, tooling defaults are wrong here — Claude Code's
`EnterWorktree` defaults to `origin/<default-branch>` — so create worktrees
explicitly and enter by path:

```bash
git worktree add .claude/worktrees/<slug> -b <slug> <base>
```

If the work genuinely needs a commit that exists only on `integration`, merge or
rebase it in. That is not a licence to re-base onto the shared branch.

## Sync with `integration` before every push

**Every push is preceded by a merge of `integration` into your branch.** Commit
your work first, then, on your branch:

```bash
git pull origin <integration>
```

Resolve every conflict, commit the merge, re-run the verify gates on the merged
tree, and only then push.

The order is not interchangeable:

1. Commit the feature work
2. `git pull origin <integration>`
3. Resolve conflicts and commit the merge
4. Run every verify gate — **on the merged tree**
5. `git push`

Why the pull comes before the gates: `integration` is where every other branch
lands, so it moves underneath you while you work. Gates that ran before the merge
verified a tree that will never exist on the remote — the merge can reintroduce a
type error, a renamed export, or a deleted helper that your branch alone was fine
with. Resolving conflicts in the PR instead means a merge commit nobody reviewed,
landing on the branch that deploys.

**No exceptions:** not for a one-line fix, not for a docs-only change, not because
you pulled an hour ago, not because the branch "can't" have diverged, and not when
`git pull` reports Already up to date — that outcome is the check passing, not
evidence the check was unnecessary. If the merge turns out to be empty, the step
cost you five seconds.

If you had to fix anything to resolve the conflicts, that fix is part of the
change: it goes through the gates like the rest, not straight to the push.

## Verify before claiming done

Run every gate in the config, in the order it lists them. Where the config marks
a gate as **not wired** — no hook, no CI job, or a runner the project hasn't
finished migrating — that gate is yours to run by hand. Nothing will catch it for
you.

Where the config marks a gate as **broken or unported**, and your change is in
the area it covers, say so explicitly in the PR. Do not report that area as
verified on the strength of the gates that did run.

Scope gates to one package while iterating if the config records a filtered
invocation. The run that counts is the one **after** the `integration` merge —
iterate as often as you like before it, but a green run from before the merge
does not release the push.

## Never `--no-verify`

The rule holds even where the config records no hooks installed. It is about not
routing around a gate, and the gates are whatever the config lists. Bypassing
only moves the failure to the remote — fix the underlying issue.

Where a specific hook blocks you, fix what it is checking rather than suppressing
it. The config records what each hook enforces and where its conventions are
documented.

## Commit format

Conventional Commits: `feat(scope): …`, `fix(scope): …`, `test(scope): …`. Body is
1–2 sentences focused on the **why**, not a restatement of the diff. Use the
scopes the config lists; if it lists none, match the scopes in `git log`.

## Before opening the PR

Check the config's generated-artifacts table. Each row pairs a trigger — a path
you touched, an API surface you changed — with the command that regenerates what
would otherwise drift. Run the ones your change triggers.

Then check the gates table for anything marked broken or unported that your
change touches, and flag the gap in the PR rather than quietly skipping it.

Working a ticket? The `plane-workflow` skill covers the comment and state
transition that follow the PR.
