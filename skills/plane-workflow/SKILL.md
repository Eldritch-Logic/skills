---
name: plane-workflow
description: Use when working a ticket tracked in Plane - starting a work item, moving it between states, planning a multi-task feature as a parent plus sub-tasks, recording commit hashes on a ticket, spawning follow-up items, or setting Plane up for a project for the first time.
---

# Plane work-item lifecycle

## Load the project config first

Read `.claude/plane-workflow.md` from the project root before any Plane call. It
holds the `project_id`, the state IDs this lifecycle refers to by role, the
verification gates, and the branch flow.

**If that file doesn't exist, initialize before doing anything else** — see
[references/initialization.md](references/initialization.md). It reads the real
values out of Plane and writes the config. Don't work a ticket from guessed IDs,
and don't hand-write UUIDs.

Plane MCP tools are namespaced per server (`mcp__plane__`, `mcp__plane-remote__`,
…); the config records the prefix. If it records `workspace_slug` as
`server-configured`, omit that argument from every call.

Where this skill names a **role** — `start`, `review`, `plan`, ship states — look
up the actual state in the config. Never move a ticket to a state by name alone.

## Per work item, in order

1. **Move it to the `start` state** — before touching code, not after.
2. **Do the work and confirm it.** Run the project's verification gates and get
   the change onto the integration branch using the `shipping-changes` skill —
   it owns the branch model, the gate list, and the pull-before-push order, and
   its config records where a gate has a known coverage gap. Where a gate can't
   cover your change, say so explicitly rather than treating the rest as
   covering it. Smoke-test where it matters.
3. **Don't skip the sync.** `shipping-changes` requires merging the integration
   branch in and re-running the gates on the merged tree before you push. Commit
   without pushing only if the user asked to batch a multi-task push; the sync
   then belongs to whichever task actually pushes.
4. **Spawn anything noteworthy as a new work item** — vestigial code paths, UX
   gaps, deprecated branches, follow-ups you flagged but didn't fix. Each one
   references the originating ticket and the commit hash that surfaced it.
   **Don't bury follow-ups in comments on the original ticket** — they go
   invisible the moment it closes.
5. **Comment on the work item** with a short summary and the commit hash(es).
6. **Move it to the `review` state** as the final step. Ship states are set later,
   as the work actually deploys — not by you at hand-off. If the config records
   `review` as `none`, stop at the comment and tell the user the ticket needs a
   state change you have no binding for.

Use only the labels in the config. If it records none, the project has none —
don't invent them. File only into the project the config names; the sibling
projects it lists are there so tickets don't land in the wrong one.

## Planning a multi-task feature

1. **Create a parent work item in the `plan` state** capturing the feature at a
   high level.
2. **Put the plan in its description** — scope, intent, proposed task breakdown.
3. **Each planned task becomes a sub-task of the parent**, not a sibling. Without
   the parent link the rollup is invisible.
4. **Each sub-task runs the full lifecycle above** independently. One commit per
   sub-task, so the hash on its comment maps 1:1 to the work.
5. **The parent moves to `review` only once every sub-task is already there** —
   check the children yourself even if the user says "we're done".
