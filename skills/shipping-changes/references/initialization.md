# Initializing shipping-changes for a project

Produces `.claude/shipping-changes.md` in the project root. Run once per project,
and again when the branch model or the gate commands change.

**Infer, then confirm.** Everything here is read out of the repository, and every
inference has a failure mode that costs more than the question would have. Show
the user what you found and what you concluded before writing the file.

## 1. Map the branch roles

```bash
git branch -a
git remote show origin | head -20        # names the remote HEAD
git log --oneline --graph --all -30      # shows what actually merges into what
```

- **`mainline`** — the production branch. Usually the remote HEAD: `main`,
  `master`, `production`.
- **`integration`** — a long-lived branch that PRs land in *before* mainline, and
  that mainline periodically merges from. Names like `develop`, `development`,
  `staging`, `next`. Confirm it by finding merge commits going *into* it from
  feature branches and *out of* it into mainline. **If no such branch exists,
  record `none`** — plenty of projects run a single protected branch, and
  inventing a second one breaks every rule that references it.
- **`base`** — what new work branches from. Default this to `integration` (or
  `mainline` when integration is `none`). Some projects branch work off a
  long-lived per-developer branch instead; you can spot that when recent feature
  branches share a parent that is neither protected branch. **Ask** rather than
  assuming — this is the field most likely to be wrong, and getting it wrong
  puts new work on the wrong lineage from the first commit.
- **`work`** — the naming pattern in recent branches: `feat/<slug>`,
  `<initials>/<slug>`, bare slugs.

Record the repository default branch separately from `mainline`. They are usually
the same, but the skill needs the default specifically, because worktree tooling
picks it and will be wrong whenever `base` differs.

Determine whether protected branches take direct pushes: if recent commits on
them are merge commits referencing PRs, PRs are required. Check branch protection
directly where you can (`gh api repos/{owner}/{repo}/branches/{branch}/protection`).

## 2. Collect the verification gates

Look in `package.json` scripts, `Makefile`, `justfile`, `pyproject.toml`,
`Cargo.toml`, `.github/workflows/*.yml`, and the project's agent instructions.

Order them cheapest-first — lint, then types, then tests — so a failure surfaces
before the slow gate runs.

For each gate, establish its **status**, which is the field that actually changes
behavior:

- `wired` — a git hook or a CI job runs it too.
- `not wired` — no hook, no CI job. The skill tells the agent to run it by hand.
- `broken` — the command exists but does not do its job. This is common
  mid-migration: a suite that hasn't been ported to a new runner, an integration
  suite nobody can run locally. **Record what it fails to cover**, not just that
  it is broken. That note is what stops a change in the uncovered area from being
  reported as verified.

Cross-check CI against local scripts. A job in `.github/workflows` with no local
equivalent is a gate that only fails after you push; a local script no CI job
runs is a gate only this skill will enforce.

Also record the filtered single-package invocation if the project has a monorepo
task runner, and a full local-CI command if one exists.

## 3. Read the hook status

```bash
ls .git/hooks | grep -v sample
cat .husky/* 2>/dev/null
git config core.hooksPath
```

Record what each hook runs and what it enforces. `none installed` is a real
answer and worth recording explicitly — it tells the next session that the gates
are entirely manual rather than leaving it to re-check.

Where a hook enforces a project convention — an i18n guard, an import boundary, a
license header — record where that convention is documented, so a blocked agent
fixes the cause instead of suppressing the check.

## 4. Find the generated artifacts

Look for committed files that a command produces: OpenAPI schemas, generated
clients, database migrations, i18n catalogs, `*.generated.*`, protobuf output,
lockfiles with dedicated scripts.

For each, record the trigger as something the agent can actually check against
its own diff — a path glob, an API surface, a specific source file — plus the
command and what drifts if it doesn't run.

A generator that CI regenerates and diffs is a `wired` gate; one nobody checks
belongs here, because otherwise the drift ships.

## 5. Record the commit scopes

```bash
git log --oneline -50
```

If the project uses Conventional Commits, extract the scopes actually in use.
If commits don't follow a convention, record no scopes — the skill falls back to
matching `git log`, and inventing a taxonomy the project doesn't use produces
commits that look out of place.

## 6. Write the config

Fill in [config-template.md](config-template.md) and write it to
`.claude/shipping-changes.md`. Create `.claude/` if needed.

If the file exists, show the user what changes before overwriting. Hand edits
outrank your inference.

## Verifying

Check the inference against the repository, not against the file you just wrote:

1. Every branch in the config resolves: `git rev-parse --verify origin/<branch>`.
2. Every gate command exists — it's a script in `package.json`, a `Makefile`
   target, a real binary. A gate that isn't runnable is worse than no gate,
   because the skill will report it as run.
3. `base` matches reality: `git log --oneline <base>..<a recent feature branch>`
   should show only that branch's work. A long unrelated history means `base` is
   wrong.

Fix anything that fails before shipping a change through this config.
