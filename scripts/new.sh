#!/usr/bin/env bash
# Scaffold a new skill, agent, command, or workflow from templates/.
#
#   scripts/new.sh skill    condition-based-waiting
#   scripts/new.sh agent    spec-reviewer
#   scripts/new.sh command  ship
#   scripts/new.sh workflow audit-deps
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  echo "usage: $(basename "$0") {skill|agent|command|workflow} <kebab-case-name>" >&2
  exit 2
}

[[ $# -eq 2 ]] || usage
kind="$1"
name="$2"

if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "error: name must be lowercase-kebab-case, got '$name'" >&2
  exit 1
fi

# Title Case From Kebab, for the H1 heading.
title="$(echo "$name" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')"

case "$kind" in
  skill)    target="$ROOT/skills/$name/SKILL.md"; template="$ROOT/templates/SKILL.md" ;;
  agent)    target="$ROOT/agents/$name.md";       template="$ROOT/templates/agent.md" ;;
  command)  target="$ROOT/commands/$name.md";     template="$ROOT/templates/command.md" ;;
  workflow) target="$ROOT/workflows/$name.js";    template="$ROOT/templates/workflow.js" ;;
  *)        usage ;;
esac

if [[ -e "$target" ]]; then
  echo "error: $target already exists" >&2
  exit 1
fi

mkdir -p "$(dirname "$target")"
sed -e "s/verb-first-skill-name/$name/g" \
    -e "s/^# Verb First Skill Name$/# $title/" \
    -e "s/^name: agent-name$/name: $name/" \
    -e "s/^You are a \[role\]/You are a [role]/" \
    -e "s/name: 'workflow-name'/name: '$name'/" \
    "$template" > "$target"

echo "created $target"
if [[ "$kind" == "skill" ]]; then
  cat <<'NEXT'

Next: before filling this in, run the baseline. Dispatch a subagent at the task
this skill is meant to govern WITHOUT the skill, and write down verbatim what it
did wrong. The skill exists to close those specific failures.
See docs/authoring-skills.md.
NEXT
fi
