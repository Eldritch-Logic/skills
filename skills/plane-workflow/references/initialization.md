# Initializing plane-workflow for a project

Produces `.claude/plane-workflow.md` in the project root. Run once per project,
and again whenever the project's states change.

**Read every ID from the API.** Project and state IDs are UUIDs — you cannot
infer, remember, or pattern-match them. A guessed ID either errors or silently
writes to the wrong project.

## 1. Find the Plane MCP server

Plane MCP tools are namespaced by the server's configured name, so the prefix
differs per session — `mcp__plane__`, `mcp__plane-remote__`, and so on. Locate
the tools available to you and use that prefix throughout. Record it in the
config so later sessions don't have to re-derive it.

No Plane MCP server connected? Stop and tell the user it must be configured
first. Don't fall back to the REST API or to guessing.

## 2. Resolve the workspace

Call `list_projects` with no arguments. If it succeeds, the server has a
workspace configured — record `workspace_slug` as `server-configured` and **omit
that argument from every later call.** If it requires an explicit workspace, ask
the user for the slug and record the literal value.

## 3. Identify the project

From the `list_projects` result, match the current repository to a project by
name or identifier. **Confirm the match with the user before writing anything** —
a plausible name match is not a confirmed one, and filing a project's tickets
into a sibling project is expensive to undo.

Record `project_id`, project name, and the ticket identifier (the `ABC` in
`ABC-123`). Record every other project in the workspace under "sibling projects"
so later sessions have an explicit do-not-file list.

## 4. Pull the states

Call `list_states` with the `project_id`. Record every state's name, `id`, and
`group` in the "all states" table.

Then map roles. Plane's five groups make the mapping mostly mechanical:

| Group | Usually the role |
| ----- | ---------------- |
| `backlog` | `plan` — where parent/feature items are created |
| `unstarted` | none — the queue tickets sit in before work starts |
| `started` | `start`, and often `review` when review is a separate started state |
| `completed` | `review` if there is no started review state; otherwise ship states |
| `cancelled` | none |

Groups are a starting point, not the answer. Projects add custom states, and the
names carry the intent the groups don't:

- **`start`** — the state meaning "someone is working this now". With several
  `started` states, it's the earliest.
- **`review`** — where a ticket lands at hand-off, awaiting someone else. Names
  like "Pending Review", "In Review", "QA", "Needs Approval".
- **Ship states** — set by a deploy or a release, not by whoever wrote the code.
  Names like "Pushed to Staging", "Released", "Deployed", "Done".

**Propose the mapping and have the user confirm it.** Show each role next to the
state you picked and the states you rejected. If a role has no sensible state,
record `none` rather than forcing a bad match — a wrong `review` binding sends
every finished ticket to the wrong place.

## 5. Pull the labels

Call `list_labels` with the `project_id`. Record what comes back. An empty result
is a real answer — record the empty table so later sessions know not to invent
labels rather than re-checking.

## 6. Record the verification gates

These come from the repository, not from Plane. Look for the project's test and
check commands in `package.json` scripts, `Makefile`, `justfile`, `pyproject.toml`,
CI workflow files, or the project's own agent instructions.

List the commands you found, say what each covers, and ask the user to confirm
and order them. Note any gate that is known-broken or has a coverage gap — the
lifecycle needs that written down, because a gap the agent can't see is a gap it
will paper over.

## 7. Record the branch flow

Infer from the repo, then confirm:

- **Integration branch** — what PRs target. Check the default branch, and whether
  a long-lived `develop`/`development`/`staging` branch exists that recent merge
  commits actually went into.
- **Working branch** — the naming pattern in `git branch -a` and recent history,
  or `direct` if commits land on the integration branch without a PR.
- **PR required** — whether recent commits arrived via merge commits or directly.

## 8. Write the config

Fill in [config-template.md](config-template.md) and write it to
`.claude/plane-workflow.md` in the project root. Create `.claude/` if needed.

If the file already exists, show the user what changes before overwriting it.
Their edits may be deliberate — a role rebound by hand outranks your inference.

Tell the user the file is team configuration and should be committed.

## Verifying

Confirm initialization worked by reading real data back, not by re-reading what
you just wrote:

1. `list_work_items` with the recorded `project_id` returns this project's tickets.
2. `get_state` with the recorded `start` and `review` `state_id`s returns the
   state names in the config.

If either fails, the config is wrong. Fix it before working a ticket.
